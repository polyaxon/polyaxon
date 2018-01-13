## cluster

Usage:

```bash
$ polyaxon cluster



Cluster info:

--------------  ----------------------------------------
build_date      2017-11-20T05:17:43Z
major           1
go_version      go1.8.3
git_version     v1.8.4
platform        linux/amd64
git_commit      9befc2b8928a9426501d3bf62f72849d5cbcd5a3
git_tree_state  clean
minor           8
compiler        gc
--------------  ----------------------------------------

Cluster Nodes:

  sequence  name                       hostname                   role    memory      n_cpus    n_gpus
----------  -------------------------  -------------------------  ------  --------  --------  --------
         1  k8s-master-13475325-0      k8s-master-13475325-0      master  6.7 Gb           2         0
         2  k8s-agentpool2-13475325-0  k8s-agentpool2-13475325-0  agent   54.93 Gb         6         1
         3  k8s-agentpool1-13475325-0  k8s-agentpool1-13475325-0  agent   6.7 Gb           2         0
```

Get cluster and nodes info.

Options:

option | type | description
-------|------|------------
  -n, --node| INTEGER| Get information about a node.
  --help| | Show this message and exit.


## node


Usage:

```bash
$ polyaxon cluster -n 2


Node info:

------------------  ---------------------------
sequence            2
name                k8s-agentpool2-13475325-0
status              Ready
hostname            k8s-agentpool2-13475325-0
role                agent
memory              54.93 Gb
n_cpus              6
n_gpus              1
kubelet_version     v1.8.4
docker_version      1.12.6
os_image            Debian GNU/Linux 8 (jessie)
kernel_version      4.11.0-1015-azure
schedulable_taints  True
schedulable_state   True
------------------  ---------------------------

Node GPUs:

  index  name       memory           serial
-------  ---------  --------  -------------
      0  Tesla K80  11.17 Gb  0321417065698
```
