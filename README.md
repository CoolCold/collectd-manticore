# purpose
collectd Exec type plugin to gather stats from Manticore ( https://manticoresearch.com )

# sample
## grafana graph


# collectd sample config
Refer to [official docs](https://collectd.org/wiki/index.php/Plugin:Exec), but in general it should work with quite simple config like that:
```
root@delta7:~# cat /etc/collectd/conf.d/10-exec.conf
# Generated by Puppet
<LoadPlugin exec>
  Globals false
</LoadPlugin>

root@delta7:~# cat /etc/collectd/conf.d/exec-config.conf
<Plugin exec>
  Exec "nobody:nogroup" "/opt/scripts/collectd/manticore.py" "test1"

</Plugin>
```
