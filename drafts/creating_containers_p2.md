Title: Creating containers - Part 2
Date: 2017-12-08 21:00
Author: JD
Category: docker 
Slug: creating-containers-part-2

In November 2014, [Michael Crosby](https://twitter.com/crosbymichael) started a series of blog posts detailing "how docker creates containers". The [first part](http://crosbymichael.com/creating-containers-part-1.html) is a great read. Unfortunately, he never got around to continuing the series. So I'm going to try to do it myself! Fair warning, though: unlike the original author, I am not an engineer at Docker. In fact, I'll be using this series of articles to learn about the inner workings of containers myself.

By the way, other people have written or talked about the nature of containers in the meantime. [This talk](https://www.youtube.com/watch?v=HPuvDm8IC-4) by Liz Rice is really good.

# About examples

I will keep using C for the examples, as in the original post. Michael's container, `crosbymichael/make-containers`, is still available, so you can still follow along the examples by running `docker run -it --privileged --net host crosbymichael/make-containers`.

For Go aficionados, [Ed King](https://twitter.com/edking2) has written a series of Medium articles on Linux Namespaces in Go ([here](https://medium.com/@teddyking/linux-namespaces-850489d3ccf)'s the first part). Still, be aware that working with namespaces in Go can be a bit tricky, because of the way Go handles concurrency. [This article](https://www.weave.works/blog/linux-namespaces-and-go-don-t-mix) by Weaveworks shows an example of how things can go bad.

Anyway, for illustrative use cases, it all works fine. Porting the C examples in Go is pretty simple; here's the Go version of Michael's `network.c`:

```go
package main

import (
	"os"
	"os/exec"
	"syscall"
)

func main() {
	cmd := exec.Command(os.Args[1], os.Args[2:]...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	cmd.Stdin = os.Stdin
	cmd.SysProcAttr = &syscall.SysProcAttr{}
	cmd.SysProcAttr.Cloneflags = syscall.CLONE_NEWNET

	// Run waits for the Command to finish. Alternative is Start then Wait
	err := cmd.Run()
	if err != nil {
		panic(err)
	}
}
```

# A quick return on part 1 examples

First, I'll quickly go over some things I noticed while going through part 1.

## MNT namespaces

As I was going through the examples of part 1, I observed some strange behavior with the MNT namespace example. When I ran it in Michael's `crosbymichael/make-containers` container, it worked as intended. But if I ran it directly on my host, a Ubuntu 17.10 VM, it did not. Instead, the newly mounted tmpfs would appear in both the namespaced "pseudo-container" and the host.

 [This StackOverflow post](https://stackoverflow.com/questions/41128296/mount-filesystem-after-clone-with-clone-newns-flag) explains the issue perfectly: on my host VM, systemd sets most of my root mount points' propagation types as MS_SHARED. Then, when I run the example, the pseudo-container inherits this, and so its filesystem, despite being in a MNT namespace, is still sharing the new changes with the host. The solution is to start by remounting the root mount point at the beginning of `child_exec`, to set its propagation type as `MS_PRIVATE` or `MS_SLAVE`:

 ```c
static int child_exec(void *stuff)
{
	struct clone_args *args = (struct clone_args *)stuff;
	if (mount("/", "/", NULL, MS_PRIVATE, "") < 0) {
		fprintf(stderr, "Cannot set MS_PRIVATE flag to root filesystem (error code %d)\n", errno);
		return -1;
	}
	if (mount("none", "/mytmp", "tmpfs", 0, "") != 0) {
			fprintf(stderr, "failed to mount tmpfs %s\n",
					strerror(errno));
			exit(-1);
	}
	if (execvp(args->argv[0], args->argv) != 0) {
			fprintf(stderr, "failed to execvp argments %s\n",
					strerror(errno));
			exit(-1);
	}
	// we should never reach here!
	exit(EXIT_FAILURE);
}
```

Then, the following changes are not "shared up" with the host. This problem did not occur in Michael's container because the propagation type is not MS_SHARED from the get go. I suppose Debian Jessie's default is different.

## PID namespaces 

The PID namespace example also failed to run on my host VM. 

The issue was with unmounting /proc, because of [binfmt_misc](https://en.wikipedia.org/wiki/Binfmt_misc), which has a mountpoint at `/proc/sys/fs/binfmt_misc`. In fact, this directory was mounted twice - huh. Maybe this is linked to [this issue](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=847788). 

The obvious solution was to unmount `/proc/sys/fs/binfmt_misc` from the new namespace, after setting the propagation type of the root mount point. Well, when I did, it also unmounted it for my host. Double-huh. I can see that [someone else](https://stackoverflow.com/questions/39864352/mount-after-clone-with-clone-newns-set-effects-parent) got the same problem, including the double-mounting. I'll check on another Linux machine when I get the chance.

Anyway, once that pesky nested mount point problem was dealt with, the example ran fine. `binfmt_misc` is not that important to me, so I guess I can live with maybe screwing it up a bit.

# User namespaces

For this first post, I'd like to complete the original part 1. The section on USER namespaces was pretty short and did not really show how user namespacing works, and what it can offer. So let's discover a bit more about it.

