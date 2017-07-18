# curl

A simple Firebase-hosted file server for install and other scripts or artifacts. Initially for the purpose of making the entire toolkit installable from a single command including installing docker, pulling the `iqtk` Docker image, and test-running it locally.

Example deployment usage:

```bash
./deploy.sh
```

Example user usage:

```bash
curl -fsSL scripts.iqtk.io/setup -o setup && sh setup
```
