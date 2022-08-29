### Cache

```bash
$ pip3 cache dir

$ pip3 cache info

$ pip3 cache list <pattern>

$ pip3 cache remove <pattern>

$ pip3 cache purge

$ pip3 install package_name --no-cache-dir
```


### Install Tensorflow


```
$ mkdir -p $TMPDIR
```

```
$ export TMPDIR=$HOME/tmp
```

```
$ TMPDIR=tmp pip3 install <package>
```

```
$ pip3 install -b $HOME/build
```

```
$ pip3 install tensorflow --no-cache-dir
```


### Install packages


```bash
$ (env) pip3 install flask flask-sqlalchemy pillow tensorflow --no-cache-dir
```
