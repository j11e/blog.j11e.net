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

As I was going through the examples of part 1, MNT namespaces
https://stackoverflow.com/questions/41128296/mount-filesystem-after-clone-with-clone-newns-flag

PID namespaces issues with unmounting /proc necause of binfmt\_misc (/proc/sys/fs/binfmt\_misc). Unmounting binfmt_misc from the new MNT namespace unmounted it for my host too. Huh.

# User namespaces




todo:
- user namespaces
- how we jail the container's processes inside a root filesystem, aka a docker image,
    chroot, pivot_root
- using cgroups
- using Linux capabilities