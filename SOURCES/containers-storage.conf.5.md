% storage.conf(5) Container Storage Configuration File
% Dan Walsh
% May 2017

# NAME
storage.conf - Syntax of Container Storage configuration file

# DESCRIPTION
The STORAGE configuration file specifies all of the available container storage options
for tools using shared container storage, but in a TOML format that can be more easily modified
and versioned.

# FORMAT
The [TOML format][toml] is used as the encoding of the configuration file.
Every option and subtable listed here is nested under a global "storage" table.
No bare options are used. The format of TOML can be simplified to:

    [table]
    option = value

    [table.subtable1]
    option = value

    [table.subtable2]
    option = value

## STORAGE TABLE

The `storage` table supports the following options:

**graphroot**=""
  container storage graph dir (default: "/var/lib/containers/storage")
  Default directory to store all writable content created by container storage programs

**runroot**=""
  container storage run dir (default: "/var/run/containers/storage")
  Default directory to store all temporary writable content created by container storage programs

**driver**=""
  container storage driver (default is "overlay")
  Default Copy On Write (COW) container storage driver

### STORAGE OPTIONS TABLE 

The `storage.options` table supports the following options:

**additionalimagestores**=[]
  Paths to additional container image stores. Usually these are read/only and stored on remote network shares.

**size**=""
  Maximum size of a container image.  Default is 10GB.  This flag can be used to set quota
  on the size of container images.

**override_kernel_check**=""
  Tell storage drivers to ignore kernel version checks.  Some storage drivers assume that if a kernel is too
  old, the driver is not supported.  But for kernels that have had the drivers backported, this flag
  allows users to override the checks

[storage.options.thinpool]

Storage Options for thinpool

The `storage.options.thinpool` table supports the following options:

**autoextend_percent**=""

Tells the thinpool driver the amount by which the thinpool needs to be grown. This is specified in terms of % of pool size. So a value of 20 means that when threshold is hit, pool will be grown by 20% of existing pool size. (Default is 20%)

**autoextend_threshold**=""

Tells the driver the thinpool extension threshold in terms of percentage of pool size. For example, if threshold is 60, that means when pool is 60% full, threshold has been hit. (80% is the default)

**basesize**=""

Specifies the size to use when creating the base device, which limits the size of images and containers. (10g is the default)

**blocksize**=""

Specifies a custom blocksize to use for the thin pool. (64k is the default)

**directlvm_device**=""

Specifies a custom block storage device to use for the thin pool. Required if you setup devicemapper

**directlvm_device_force**=""

Tells driver to wipe device (directlvm_device) even if device already has a filesystem.  Default is False

**fs**="xfs"

Specifies the filesystem type to use for the base device. (Default is xfs)

**log_level**=""

Sets the log level of devicemapper.

    0: LogLevelSuppress 0 (Default)
    2: LogLevelFatal
    3: LogLevelErr
    4: LogLevelWarn
    5: LogLevelNotice
    6: LogLevelInfo
    7: LogLevelDebug

**min_free_space**=""

Specifies the min free space percent in a thin pool require for new device creation to succeed. Valid values are from 0% - 99%. Value 0% disables (10% is the default)

**mkfsarg**=""

Specifies extra mkfs arguments to be used when creating the base device.

**mountopt**=""

Specifies extra mount options used when mounting the thin devices.

**use_deferred_removal**=""

Marks device for deferred removal.  If the device is in use when it driver attempts to remove it, driver will tell the kernel to remove it as soon as possible.  (Default is true).

**use_deferred_deletion**=""

Marks device for deferred deletion. If the device is in use when it driver attempts to delete it, driver continue to attempt to delete device every 30 seconds, or when it restarts.  (Default is true).

**xfs_nospace_max_retries**=""

Specifies the maximum number of retries XFS should attempt to complete IO when ENOSPC (no space) error is returned by underlying storage device. (Default is 0, which means to try continuously.

# HISTORY
May 2017, Originally compiled by Dan Walsh <dwalsh@redhat.com>
Format copied from crio.conf man page created by Aleksa Sarai <asarai@suse.de>
