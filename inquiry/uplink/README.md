# uplink

Simple wrapper for `gsutil rsync` that logs to Google Cloud Logging and re-tries at regular intervals.

# Installation and configuration

The tool can be installed with the following command:

```bash
curl https://raw.githubusercontent.com/cwbeitel/uplink/master/setup.sh | sh
```

You will then need to activate a service account with permission to access to the target bucket and cloud logging. This can be done with the following where `account` is the email address of the service account and `key_file` is the path to the service account private key file.

```bash
gcloud auth activate-service-account [account] --key-file=[key_file]
```

# Example

Help can be displayed with `uplink --help`. Let's suppose we have a directory named 'example' where files will be landing periodically which we want to sync to 'gs://[your-bucket]/[your-target-path]' on Google Cloud Storage. And suppose we want to wait 30s after a previously finished sync or sync attempt before re-trying a sync - such as to sync additional newly created files. The command to do so is as follows:

```bash
uplink -l /path/to/example -r gs://[your-bucket]/[your-target-path] -r 30
```

© Regents of the University of California, 2017. Licensed under a BSD-3. See [license](LICENSE).
