# Podman CI flake digest — 2026-08-13
Window: 2026-08-04T00:49:41Z → 2026-08-13T21:00:13Z · workflow `ci.yml` · repo `podman-container-tools/podman`
## Volume
- runs analyzed (completed, non-`action_required`): **174**
- runs needing >1 attempt: **64** (37%)
- confirmed flakes (job FAIL→PASS at identical commit): **62**
> Detection is attempt-diff based (`/jobs?filter=all`). A `?status=failure`
> listing cannot see re-run-to-green runs at all, and a green re-run alone is
> treated as *observation*, not proof — classification comes from log evidence.
## Failure clusters
### TEST_BUG (0.95, llm) — 37 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `not ok N |065| podman cp file from host to container volume in DUR | # `is "$output" ""' failed`
- evidence: `#|     FAIL: podman cp /tmp/podman_bats.LV9tPd/cp-test-volume/hostfile c-cp_t132-scnkbc3k:/tmp/volume/sub-volume`
- note: The failure indicates a problem with the `podman cp` command not producing the expected output. This suggests an issue in the test logic or the expected behavior.
- jobs: sys local root debian-sid,sys remote root fedora-rawhide,sys local rootless fedora-current,sys local root fedora-rawhide,sys remote rootless fedora-current,sys remote root fedora-current,sys local rootless fedora-prior,sys local root fedora-prior,sys remote root fedora-prior,sys remote root debian-sid,sys local rootless fedora-rawhide,sys local root fedora-current,sys local rootless debian-sid
- seen: 2026-08-12 → 2026-08-12
### NETWORK_INFRA (1.00, regex) — 25 occurrence(s) · 16 re-run-confirmed
- signature: `curl: (22) The requested URL returned error: 503`
- evidence: `curl: (22) The requested URL returned error: 503`
- note: external URL fetch returned a 5xx
- jobs: build fedora-rawhide,build debian-sid,bud local root fedora-current,machine linux amd64,bindings  root fedora-current,unit  root fedora-current,compose_v2  root fedora-current,apiv2  rootless fedora-current,apiv2  root fedora-current,sys local rootless debian-sid,int local rootless fedora-prior,int local root fedora-current,int local root fedora-prior,sys local root fedora-rawhide,sys local rootless fedora-prior,int remote rootless fedora-current,compose_v2  rootless fedora-current,sys local root fedora-current,int local root debian-sid
- seen: 2026-08-12 → 2026-08-12
### HARNESS (1.00, regex) — 12 occurrence(s)
- signature: `make: *** [localmachine] Error 2`
- evidence: `make: *** [localmachine] Error 2`
- note: make target failed
- jobs: macos machine applehv
- seen: 2026-08-04 → 2026-08-13
### NETWORK_INFRA (1.00, regex) — 10 occurrence(s) · 7 re-run-confirmed
- signature: `curl: (56) Connection died, tried 5 times before giving up`
- evidence: `curl: (56) Connection died, tried 5 times before giving up`
- note: connection died mid-transfer
- jobs: build fedora-current,build fedora-rawhide,build debian-sid,int local rootless fedora-current,int local root fedora-rawhide,bud local root fedora-current,int remote root debian-sid,sys remote root fedora-prior,int local rootless debian-sid
- seen: 2026-08-12 → 2026-08-12
### VM_INFRA (0.90, llm) — 8 occurrence(s)
- signature: `Error: building at STEP "RUN ip addr": opening seccomp profile failed: open /etc/containers/seccomp.json: no such file or directory`
- evidence: `Error: building at STEP "RUN ip addr": opening seccomp profile failed: open /etc/containers/seccomp.json: no such file or directory`
- note: The failure indicates an issue related to the VM environment attempting to access the seccomp profile file, which is necessary for operating in a containerized environment. This suggests a problem with the virtual machine infrastructure setup.
- jobs: machine linux amd64
- seen: 2026-08-11 → 2026-08-13
### TEST_TIMEOUT (1.00, regex) — 5 occurrence(s)
- signature: `[TIMEDOUT] A suite timeout occurred`
- evidence: `[TIMEDOUT] A suite timeout occurred`
- note: suite deadline expired; the named spec is whichever was in flight, not the culprit
- jobs: windows machine hyperv
- seen: 2026-08-05 → 2026-08-13
### NETWORK_INFRA (1.00, regex) — 5 occurrence(s) · 3 re-run-confirmed
- signature: `curl: (6) Could not resolve host: www.redhat.com`
- evidence: `curl: (6) Could not resolve host: www.redhat.com`
- note: curl failure fetching an external resource
- jobs: int local root fedora-rawhide,int remote rootless fedora-current,int local rootless fedora-current,int local root fedora-prior,int remote root fedora-prior
- seen: 2026-08-04 → 2026-08-12
### TEST_BUG (0.90, llm) — 5 occurrence(s) · 1 re-run-confirmed
- signature: `not ok N |220| podman healthcheck in DUR | # `assert "$output" =~ "StartLimitIntervalUSec=0" "The hc service has the right interval set"' failed`
- evidence: ``assert "$output" =~ "StartLimitIntervalUSec=0" "The hc service has the right interval set"' failed`
- note: The failure is due to an assertion check failing in the test for the healthcheck service configuration. This indicates a potential bug in the test itself regarding the expectations set on the healthcheck parameters.
- jobs: sys remote root fedora-current,sys local rootless debian-sid,sys local root debian-sid,sys remote root fedora-rawhide,sys local rootless fedora-current
- seen: 2026-08-13 → 2026-08-13
### NETWORK_INFRA (1.00, regex) — 4 occurrence(s) · 2 re-run-confirmed
- signature: `curl: (52) Empty reply from server`
- evidence: `curl: (52) Empty reply from server`
- note: curl failure fetching an external resource
- jobs: windows installer wsl,windows machine wsl
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 4 occurrence(s) · ⚠ confined to branch `fix-25362-config-log-level`, never re-run to green — likely that PR's regression, not a flake
- signature: `not ok N [800] podman --module - command-line completion in DUR | # `assert "${lines[0]}" = "--module=" "completion ignores the incomplete early flag"' failed`
- evidence: `Completion ended with directive: ShellCompDirectiveNoFileComp`
- note: The failure indicates an issue with command-line completion not handling flags properly, suggesting a bug in the test related to the functionality being tested.
- jobs: sys local rootless fedora-current,sys local rootless debian-sid,sys local rootless fedora-prior,sys local rootless fedora-rawhide
- seen: 2026-08-10 → 2026-08-10
### VM_INFRA (1.00, llm) — 3 occurrence(s)
- signature: `Error: machine did not transition into running state: ssh error: ssh: handshake failed: read tcp 127.0.0.1:NUM->127.0.0.1:NUM: wsarecv: An existing connection was forcibly closed by the remote host.`
- evidence: `Error: machine did not transition into running state: ssh error: ssh: handshake failed: read tcp 127.0.0.1:51788->127.0.0.1:51692: wsarecv: An existing connection was forcibly closed by the remote host.`
- note: The failure is related to the virtual machine not starting properly due to an SSH error, indicating a problem with the VM infrastructure.
- jobs: windows machine hyperv
- seen: 2026-08-06 → 2026-08-13
### PRODUCT_RACE (0.90, llm) — 2 occurrence(s)
- signature: `# Error: bogus: image not known`
- evidence: `Error: retrieving label for image "3866529f8180390e95c2c550029114a2b3f86ccc9986508b3df1e33b7ef12a66": you may need to remove the image to resolve the error: fallback error checking whether image is a manifest list: choosing image instance: no image found in manifest list for architecture "amd64", variant "", OS "linux": choosing image instance: no image found in manifest list for architecture "amd64", variant "", OS "linux"`
- note: The log indicates an error with retrieving the label for an image, suggesting a potential race condition in managing image manifests. The system attempts to find an image that isn't available for the specified architecture, which aligns with issues typically seen in product races.
- jobs: sys remote rootless fedora-current,sys remote root fedora-prior
- seen: 2026-08-11 → 2026-08-12
### NETWORK_INFRA (0.90, llm) — 2 occurrence(s)
- signature: `# Error: cannot bind tcp port 127.0.0.1:NUM: address already in use`
- evidence: `Error: cannot bind tcp port 127.0.0.1:5400: address already in use`
- note: The failure is related to an inability to bind a TCP port due to it already being in use, which indicates a networking issue.
- jobs: sys remote root fedora-rawhide,sys local root fedora-rawhide
- seen: 2026-08-11 → 2026-08-11
### NETWORK_INFRA (1.00, llm) — 2 occurrence(s) · 1 re-run-confirmed
- signature: `# Error: cannot bind tcp port :NUM: address already in use`
- evidence: `Error: cannot bind tcp port :5113: address already in use`
- note: The failure is due to an attempt to bind a TCP port that is already in use, indicating a network-related issue.
- jobs: sys local root debian-sid,sys local root fedora-rawhide
- seen: 2026-08-10 → 2026-08-10
### PRODUCT_RACE (0.80, llm) — 2 occurrence(s)
- signature: `# Error: copying layers and metadata for container "HEX": committing the finished image: creating image "HEX": layer not known`
- evidence: `Error: copying layers and metadata for container "10c0892a5bd08954b21cff001d223e1dc78a09b4f159df132ab22e497c73695a": committing the finished image: creating image "fcbdcb271e5e194ec13410884753fdc9bad59a23d1853299fbf33e5f8f34ba59": layer not known`
- note: The error indicates that the system was unable to find a required layer while attempting to commit an image. This suggests a possible race condition with layer availability when multiple jobs or processes are interacting with the same image layers.
- jobs: sys remote root debian-sid,sys local rootless fedora-current
- seen: 2026-08-13 → 2026-08-13
### VM_INFRA (0.90, llm) — 2 occurrence(s) · 1 re-run-confirmed
- signature: `# Error: copying layers and metadata for container "HEX": writing blob: adding layer with blob "sha256:HEX"/""/"sha256:HEX": unpacking failed (error: exit status 1; output: mkdir /run: no such file or directory)`
- evidence: `Error: copying layers and metadata for container "37481f2a084f2b1d81bf68b96f4929c855d8cc0d21373894979aa639ea4c705d": writing blob: adding layer with blob "sha256:7a1f38344bac66726e3bbd2ac3217101b7ca44da0192dcd0b137e0ce70e36e1a"/""/"sha256:7a1f38344bac66726e3bbd2ac3217101b7ca44da0192dcd0b137e0ce70e36e1a": unpacking failed (error: exit status 1; output: mkdir /run: no such file or directory)`
- note: The failure is related to the inability to create the required directory during the container layer unpacking, indicating an issue with the virtual machine infrastructure. The specific error message points to a missing directory that is critical for the container's operation.
- jobs: sys local root debian-sid,sys local root fedora-rawhide
- seen: 2026-08-13 → 2026-08-13
### TEST_BUG (0.90, llm) — 2 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Error: `/usr/bin/crun checkpoint --image-path /tmp/podman-e2e-X --work-path /tmp/podman-e2e-X HEX` failed: exit status 1`
- evidence: `[FAILED] Expected
      <string>: 1777 1786525282
  to equal
      <string>: 1777 1566297043`
- note: The test failure indicates an unexpected value comparison, suggesting a potential bug in the test logic or the product's handling of named volumes.
- jobs: int local root fedora-current,int local root fedora-prior
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 2 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Error: crun: (00.NUM) Error (criu/cgroup.c:NUM): cg: cgroupd: recv req error: No such file or directory: OCI runtime attempted to invoke a command that was not found`
- evidence: `time="2026-08-12T09:05:30Z" level=warning msg="StopSignal SIGTERM failed to stop container priceless_carson in 10 seconds, resorting to SIGKILL"`
- note: The error indicates a failure in the stop signal mechanism during a test which is characteristic of a bug in the test or product. The message suggests that the expected behavior (gracefully stopping the container) did not occur.
- jobs: int local root debian-sid,int local root fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### VM_INFRA (0.90, llm) — 2 occurrence(s) · 1 re-run-confirmed
- signature: `Error: machine did not transition into running state: ssh error: machine not in running state`
- evidence: `Error: machine did not transition into running state: ssh error: machine not in running state`
- note: The failure indicates that the virtual machine did not change to a running state due to an SSH error, suggesting an issue with the VM infrastructure handling.
- jobs: windows machine wsl
- seen: 2026-08-06 → 2026-08-13
### VM_INFRA (0.90, llm) — 2 occurrence(s) · 1 re-run-confirmed
- signature: `Error: machine did not transition into running state: ssh error: ssh: handshake failed: read tcp 127.0.0.1:NUM->127.0.0.1:NUM: read: connection reset by peer`
- evidence: `Error: machine did not transition into running state: ssh error: ssh: handshake failed: read tcp 127.0.0.1:64180->127.0.0.1:64153: read: connection reset by peer`
- note: The failure appears to be related to the virtual machine not successfully transitioning to a running state due to an SSH handshake issue, indicating a problem with the VM infrastructure.
- jobs: macos machine libkrun
- seen: 2026-08-11 → 2026-08-13
### TEST_TIMEOUT (1.00, llm) — 2 occurrence(s)
- signature: `Error: ssh: handshake failed: read tcp 127.0.0.1:NUM->127.0.0.1:NUM: wsarecv: An existing connection was forcibly closed by the remote host.`
- evidence: `[TIMEDOUT] podman machine start [It] start simple machine`
- note: The log indicates that the test 'podman machine start' timed out. This suggests the failure is due to the test exceeding its allowed runtime.
- jobs: windows machine hyperv
- seen: 2026-08-11 → 2026-08-13
### TEST_BUG (0.90, llm) — 2 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `not ok N [23-containersArchive] POST exec/HEX/start [-d {}] : output`
- evidence: `not ok 1322 [23-containersArchive] POST exec/5157921528ff16573c22b9fa2564c93d192dc2c9d6f0a2c2891851676f70558d/start [-d {}] : output`
- note: The output shows a test failure due to unexpected output for the exec start call, indicating a potential bug in the test itself.
- jobs: apiv2  root fedora-current,apiv2  rootless fedora-current
- seen: 2026-08-07 → 2026-08-07
### TEST_TIMEOUT (1.00, llm) — 2 occurrence(s)
- signature: `not ok N bud-github-context-with-branch-subdir-commit | # `run_buildah build $WITH_POLICY_JSON -t ${target} "${gitrepo}"' failed`
- evidence: `[ rc=124 (** EXPECTED 0 **) ]`
- note: The log explicitly indicates that the process timed out, as shown by the error code 124, which is greater than 0. This directly supports the classification of a test timeout.
- jobs: bud local root fedora-current,bud remote root fedora-current
- seen: 2026-08-12 → 2026-08-12
### NETWORK_INFRA (1.00, llm) — 1 occurrence(s)
- signature: `# Error: Get "https://raw.githubusercontent.com/containers/podman/main/test/build/from-scratch/Dockerfile": net/http: TLS handshake timeout`
- evidence: `Error: Get "https://raw.githubusercontent.com/containers/podman/main/test/build/from-scratch/Dockerfile": net/http: TLS handshake timeout`
- note: The failure is due to a TLS handshake timeout while trying to access a remote resource, indicating a network-related issue.
- jobs: sys local rootless fedora-rawhide
- seen: 2026-08-07 → 2026-08-07
### TEST_BUG (0.80, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `# Error: committing container for step {Env:[PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin] Command:run Args:[mkdir /mountroot && echo data file inside the IMAGE - JrNUTk4NW3mEXYc > /mountroot/data] Flags:[] Attrs:map[] Message:RUN mkdir /mountroot && echo data file inside the IMAGE - JrNUTk4NW3mEXYc > /mountroot/data Heredocs:[] Original:RUN mkdir /mountroot && echo data file inside the IMAGE - JrNUTk4NW3mEXYc > /mountroot/data}: copying layers and metadata for container "HEX": writing blob: adding layer with blob "sha256:HEX"/""/"sha256:HEX": unpacking failed (error: exit status 1; output: mkdir /mountroot: no such file or directory)`
- evidence: `Error: committing container for step {Env:[PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin] Command:run Args:[mkdir /mountroot && echo data file inside the IMAGE - JrNUTk4NW3mEXYc > /mountroot/data] Flags:[] Attrs:map[] Message:RUN mkdir /mountroot && echo data file inside the IMAGE - JrNUTk4NW3mEXYc > /mountroot/data Heredocs:[] Original:RUN mkdir /mountroot && echo data file inside the IMAGE - JrNUTk4NW3mEXYc > /mountroot/data}: copying layers and metadata for container "21d4d48f6471c65838dd3008d513a7d72c9fab91941a601e1e478f8a9cdaf21e": writing blob: adding layer with blob "sha256:ad683f72dfe3b991d278c7beed528d6cd92d7ba768330709db42161b0f142664"/""/"sha256:11da3b82027e1ffdbd863db8dfcb8c70376847ab320fda2eea0e5504815653c0": unpacking failed (error: exit status 1; output: mkdir /mountroot: no such file or directory)`
- note: The error indicates that the test script tried to create a directory that does not exist, which is a failure due to an issue in the test logic or setup. This suggests there may be a bug in the test itself rather than an environmental issue.
- jobs: sys local rootless debian-sid
- seen: 2026-08-09 → 2026-08-09
### VM_INFRA (0.80, llm) — 1 occurrence(s)
- signature: `# Error: container HEX is the service container of pod(s) HEX and cannot be removed without removing the pod(s)`
- evidence: `Error: killing container 81648c4831f1f88c31d05ad326fac6b0a743a69b0e8c3f7ed35e80825ae4a573: committing transaction to add exit code: disk I/O error: resource temporarily unavailable`
- note: The error indicates a disk I/O issue, suggesting a problem with the underlying virtual machine infrastructure or storage system. Such errors are typically indicative of infrastructure-level resource availability issues.
- jobs: sys local rootless debian-sid
- seen: 2026-08-10 → 2026-08-10
### RUNNER_INFRA (0.80, llm) — 1 occurrence(s) · ⚠ confined to branch `fix-xfs-quota-selinux`, never re-run to green — likely that PR's regression, not a flake
- signature: `# Error: copying layers and metadata for container "HEX": writing blob: adding layer with blob "sha256:HEX"/""/"sha256:HEX": lstat /home/ubuntu.guest/.local/share/containers/storage/overlay/tempdirs/temp-dir-NUM/0-addition: no such file or directory`
- evidence: `Error: copying layers and metadata for container "0a8a8797ec1075461d7ad0b4ce05985a714fd4cf415566cf09be0882a9fc4bfb": writing blob: adding layer with blob "sha256:26d4ed1d17075cce1b19308d3d016b2d189eee732597e17d4774a9e0b5766855"/""/"sha256:26d4ed1d17075cce1b19308d3d016b2d189eee732597e17d4774a9e0b5766855": lstat /home/ubuntu.guest/.local/share/containers/storage/overlay/tempdirs/temp-dir-1024368511/0-addition: no such file or directory`
- note: The error indicates that a required file or directory for copying container layers is missing, which is indicative of an issue with the runner's environment or configuration. This type of failure is typically categorized under runner infrastructure problems.
- jobs: sys local rootless fedora-rawhide
- seen: 2026-08-11 → 2026-08-11
### PRODUCT_RACE (0.80, llm) — 1 occurrence(s)
- signature: `# Error: copying layers and metadata for container "HEX": writing blob: adding layer with blob "sha256:HEX"/""/"sha256:HEX": unpacking failed (error: exit status 1; output: mkdir /etc: no such file or directory)`
- evidence: `Error: copying layers and metadata for container "3427afc489760d17f43a4503c42d468705ce05b3ebff6cd329abfbe3c23fa1cc": writing blob: adding layer with blob "sha256:5cc10b26f6d9a4f7b70146bc7ab102086fff247ba024a0dc4fcc67eeae7a4066"/""/"sha256:5cc10b26f6d9a4f7b70146bc7ab102086fff247ba024a0dc4fcc67eeae7a4066": unpacking failed (error: exit status 1; output: mkdir /etc: no such file or directory)`
- note: The error indicates that the system attempted to create a directory that does not exist, which suggests a race condition where the necessary environment or resources were not available when the operation was attempted.
- jobs: sys local root fedora-rawhide
- seen: 2026-08-09 → 2026-08-09
### VM_INFRA (0.90, llm) — 1 occurrence(s)
- signature: `# Error: unable to copy from source docker-archive:/tmp/podman_bats.Udbsfa/archive.tar: writing blob: adding layer with blob "sha256:HEX"/""/"sha256:HEX": unpacking failed (error: exit status 1; output: mkdir /run: no such file or directory)`
- evidence: `Error: unable to copy from source docker-archive:/tmp/podman_bats.Udbsfa/archive.tar: writing blob: adding layer with blob "sha256:177c93835bbf5723a8e6814ee2776d85ea9c143672110317ac7f150699dbf36a"/""/"sha256:177c93835bbf5723a8e6814ee2776d85ea9c143672110317ac7f150699dbf36a": unpacking failed (error: exit status 1; output: mkdir /run: no such file or directory)`
- note: The failure indicates an issue with the VM infrastructure related to directory access or existence, particularly with the '/run' directory not being present. This typically suggests a misconfiguration or an environment issue within the virtual machine setup.
- jobs: sys local root fedora-rawhide
- seen: 2026-08-11 → 2026-08-11
### PRODUCT_RACE (1.00, regex) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `# Error: unable to obtain cgroup stats: read /sys/fs/cgroup/machine.slice/libpod-HEX.scope/memory.stat: no such device`
- evidence: `# Error: unable to obtain cgroup stats: read /sys/fs/cgroup/machine.slice/libpod-3520a47b3703d9acad1d634c887ba84d666ec693a48ab18a1a8677789f69149e.scope/memory.stat: no such device`
- note: cgroup removed between existence check and read (stats ENODEV race)
- jobs: sys local root fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### HARNESS (1.00, llm) — 1 occurrence(s) · ⚠ confined to branch `config-port`, never re-run to green — likely that PR's regression, not a flake
- signature: `# Error: unmarshalling into &types.PlayKubeReport{Pods:[]types.PlayKubePod(nil), Volumes:[]types.PlayKubeVolume(nil), PlayKubeTeardown:types.PlayKubeTeardown{StopReport:[]*types.PodStopReport{(*types.PodStopReport)(0xa43e90d8680)}, RmReport:[]*types.PodRmReport{(*types.PodRmReport)(0xa43e8e92510)}, VolumeRmReport:[]*types.VolumeRmReport(nil), SecretRmReport:[]*types.SecretRmReport{}}, Secrets:[]types.PlaySecret(nil), ServiceContainerID:"", ValidationWarnings:[]string(nil), ExitCode:(*int32)(nil)}, data "{\"Pods\":null,\"Volumes\":null,\"StopReport\":[{\"Errs\":[\"stopping container HEX: committing transaction to add exit code: disk I/O error: resource temporarily unavailable\",\"stopping container HEX: a container that depends on container HEX could not be stopped: container state improper\"],\"Id\":\"HEX\",\"RawInput\":\"liveness-exec-t459-kgiybdrv-unhealthy\"}],\"RmReport\":[{\"RemovedCtrs\":{\"HEX\":null,\"HEX\":null},\"Err\":null,\"Id\":\"HEX\"}],\"VolumeRmReport\":null,\"SecretRmReport\":[],\"Secrets\":null,\"ServiceContainerID\":\"\",\"ValidationWarnings\":null,\"ExitCode\":null}\n": json: cannot unmarshal string into Go struct field PodStopReport.PlayKubeTeardown.StopReport.Errs of type error`
- evidence: `FAIL: exit code is 125; expected 0`
- note: The failure is due to an unexpected exit code indicating a problem with the test harness, rather than a genuine issue with the product or its usage.
- jobs: sys remote rootless fedora-current
- seen: 2026-08-11 → 2026-08-11
### NETWORK_INFRA (1.00, llm) — 1 occurrence(s)
- signature: `# [TIME] Error: cannot bind tcp port :NUM: address already in use`
- evidence: `Error: cannot bind tcp port :5453: address already in use`
- note: The failure is due to a networking issue where the specified TCP port is already in use, preventing the podman network reload from succeeding.
- jobs: sys local root fedora-prior
- seen: 2026-08-04 → 2026-08-04
### RUNNER_INFRA (1.00, regex) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `##[error]Failed to run: Error: Unexpected HTTP response: 503, Error: Unexpected HTTP response: 503`
- evidence: `##[error]Failed to run: Error: Unexpected HTTP response: 503, Error: Unexpected HTTP response: 503`
- note: runner provisioning/communication failure
- jobs: Validate source code changes
- seen: 2026-08-12 → 2026-08-12
### RUNNER_INFRA (1.00, regex) — 1 occurrence(s)
- signature: `##[error]Failed to run: Error: socket hang up, Error: socket hang up`
- evidence: `##[error]Failed to run: Error: socket hang up, Error: socket hang up`
- note: runner provisioning/communication failure
- jobs: Validate source code changes
- seen: 2026-08-12 → 2026-08-12
### VM_INFRA (0.90, llm) — 1 occurrence(s)
- signature: `Error: EOF`
- evidence: `Error: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ: VM does not exist`
- note: The failure indicates that the specified virtual machine does not exist, pointing to a problem related to VM infrastructure.
- jobs: macos machine applehv
- seen: 2026-08-12 → 2026-08-12
### TEST_TIMEOUT (1.00, llm) — 1 occurrence(s) · ⚠ confined to branch `bump-6.1.1-dev`, never re-run to green — likely that PR's regression, not a flake
- signature: `Error: Post "http://localhost:PORT/vm/state": EOF`
- evidence: `[FAILED] Timed out after 600.001s.`
- note: The failure is explicitly related to a command timing out after a specified duration. This indicates that the test did not complete within the expected time frame.
- jobs: macos machine applehv
- seen: 2026-08-12 → 2026-08-12
### PARALLEL_INTERFERENCE (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `Error: committing container for step {Env:[PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin] Command:run Args:[touch rmtest:0] Flags:[] Attrs:map[] Message:RUN touch rmtest:0 Heredocs:[] Original:RUN touch rmtest:0}: copying layers and metadata for container "HEX": writing blob: adding layer with blob "sha256:HEX"/""/"sha256:HEX": unpacking failed (error: exit status 1; output: open /rmtest:0: no such file or directory)`
- evidence: `Error: committing container for step {Env:[PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin] Command:run Args:[touch rmtest:0] Flags:[] Attrs:map[] Message:RUN touch rmtest:0 Heredocs:[] Original:RUN touch rmtest:0}: copying layers and metadata for container "04c35a389d8291aca95228f3ec9f1fd9d671f2b7e963f60973aaaa1690fb2315": writing blob: adding layer with blob "sha256:724a7a770a18a396d836f1d9f138d4d59bc7ccbdcdb52e537e092b917934fa7b"/""/"sha256:58b0aee591ec4897a5508c869395001c63a3e009a77616e68259c57d01af47ad": unpacking failed (error: exit status 1; output: open /rmtest:0: no such file or directory)`
- note: The error indicates a failure related to concurrent operations attempting to modify or access the same resources, specifically layers in an image build. This suggests a potential interference between parallel test executions.
- jobs: int local root fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### NETWORK_INFRA (1.00, llm) — 1 occurrence(s) · ⚠ confined to branch `renovate/golang.org-x-net-0.x`, never re-run to green — likely that PR's regression, not a flake
- signature: `Error: downloading URL "archive": invalid response status 503`
- evidence: `Error: downloading URL "archive": invalid response status 503`
- note: The failure is due to an invalid response status (503) when trying to download a URL, indicating a network-related issue with accessing the resource.
- jobs: int remote root fedora-prior
- seen: 2026-08-12 → 2026-08-12
### UNKNOWN (0.00, llm) — 1 occurrence(s)
- signature: `Error: failed to remove machines files: remove C:\Users\RUNNER~1\AppData\Local\Temp\podman_test2722611864\.local\share\containers\podman\machine\hyperv\HEX-amd64.vhdx: The process cannot access the file because it is being used by another process.`
- jobs: windows machine hyperv
- seen: 2026-08-12 → 2026-08-12
### VM_INFRA (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `renovate/golang.org-x-net-0.x`, never re-run to green — likely that PR's regression, not a flake
- signature: `Error: failed to remove machines files: remove C:\Users\RUNNER~1\AppData\Local\Temp\podman_test4253939334\.local\share\containers\podman\machine\hyperv\HEX-amd64.vhdx: The process cannot access the file because it is being used by another process.`
- evidence: `The process cannot access the file because it is being used by another process.`
- note: The error indicates an issue with accessing a virtual machine file, suggesting a problem in the virtual machine infrastructure. This aligns with VM infrastructure failures typically associated with resource contention.
- jobs: windows machine hyperv
- seen: 2026-08-12 → 2026-08-12
### VM_INFRA (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `Error: krunkit exited unexpectedly with exit code 1`
- evidence: `Error: krunkit exited unexpectedly with exit code 1`
- note: The failure is due to 'krunkit' exiting unexpectedly, which indicates a potential issue with the virtual machine infrastructure used by the Podman project.
- jobs: macos machine libkrun
- seen: 2026-08-12 → 2026-08-12
### VM_INFRA (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `renovate/github.com-sirupsen-logrus-1.x`, never re-run to green — likely that PR's regression, not a flake
- signature: `Error: machine did not transition into running state: ssh error: machine is not listening on ssh port`
- evidence: `Error: machine did not transition into running state: ssh error: machine is not listening on ssh port`
- note: The failure indicates issues with the virtual machine not being able to start properly due to SSH connection problems, suggesting a problem with VM infrastructure.
- jobs: windows machine wsl
- seen: 2026-08-13 → 2026-08-13
### NETWORK_INFRA (1.00, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `Error: pasta failed with exit code 1:`
- evidence: `Listen failed for HOST TCP port */39951: Address already in use`
- note: The failure indicates that the test could not bind to a TCP port because it was already in use, suggesting a network resource issue.
- jobs: int local rootless fedora-prior
- seen: 2026-08-11 → 2026-08-11
### TEST_TIMEOUT (0.90, llm) — 1 occurrence(s)
- signature: `Error: unable to copy from source docker://quay.io/libpod/testimage:NUM: copying system image from manifest list: parsing image configuration: Get "https://cdn01.quay.io/quayio-production-s3/sha256/b8/HEX?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIATAAF2YHTGR23ZTE6%2F20260805%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260805T100727Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=HEX&region=us-east-1&namespace=libpod&repo_name=testimage&akamai_signature=exp=NUM~hmac=HEX": remote error: tls: internal error`
- evidence: `[TIMEDOUT] podman machine list [It] list machine: check if running while starting`
- note: The log indicates that a suite timeout occurred during a test that checks if the machine is running while starting. This suggests that the test exceeded its allotted time limit.
- jobs: windows machine hyperv
- seen: 2026-08-05 → 2026-08-05
### VM_INFRA (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `Error: unable to start "m2-HEX": m1-HEX already starting or running: only one VM can be active at a time`
- evidence: `Error: unable to start "m2-b9a25a28f240": m1-7a530e072381 already starting or running: only one VM can be active at a time`
- note: The failure is specifically related to virtual machine constraints, indicating that the test attempts to start multiple VMs simultaneously, which is not allowed.
- jobs: macos machine libkrun
- seen: 2026-08-10 → 2026-08-10
### TEST_TIMEOUT (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/hyperv-vsock-ready-timeout`, never re-run to green — likely that PR's regression, not a flake
- signature: `Error: unsupported provider "wsl"`
- evidence: `[FAILED] Timed out after 600.000s.`
- note: The log indicates that a test failed due to a timeout after 600 seconds, suggesting that the test did not complete in the expected timeframe.
- jobs: macos machine applehv
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [3.967 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:54 . dr-xr-xr-x 1 root root 100 Aug 12 06:54 .. -rw------- 1 root root 0 Aug 12 06:54 3447821163
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected ownership of the file did not match the actual ownership, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int local rootless debian-sid
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.153 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 09:03 . dr-xr-xr-x 1 root root 100 Aug 12 09:03 .. -rw------- 1 root root 0 Aug 12 09:03 2034608130
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int local rootless fedora-current
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.205 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:17 . dr-xr-xr-x 1 root root 100 Aug 12 06:17 .. -rw-------    1 root     root             0 Aug 12 06:17 3212941761
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected ownership of the file did not match the actual ownership, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int local rootless debian-sid
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.278 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:56 . dr-xr-xr-x 20 root root 400 Aug 12 06:56 .. -rw------- 1 root root 0 Aug 12 06:56 4075774064
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential issue in the test logic or the code being tested. The expectation of user IDs in the output suggests a bug in the handling of file permissions or ownership.
- jobs: int local rootless fedora-prior
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.320 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:52 . dr-xr-xr-x 1 root root 100 Aug 12 06:52 .. -rw------- 1 root root 0 Aug 12 06:52 3920719748
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected ownership of the files in the volume did not match the actual ownership, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int remote rootless fedora-current
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.347 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 07:04 . dr-xr-xr-x 1 root root 100 Aug 12 07:04 .. -rw------- 1 root root 0 Aug 12 07:04 22322618
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential issue in the test logic or the code being tested. The expectation that the output should contain '9999 9999' suggests a bug in the test rather than an environmental issue.
- jobs: int local root fedora-current
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.353 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 09:06 . dr-xr-xr-x 1 root root 100 Aug 12 09:06 .. -rw------- 1 root root 0 Aug 12 09:06 2779435220
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int remote rootless fedora-current
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.364 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 09:00 . dr-xr-xr-x 1 root root 100 Aug 12 09:00 .. -rw------- 1 root root 0 Aug 12 09:00 1792177060
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential issue in the test logic or the code being tested. The expectation that the output should contain '9999 9999' suggests a bug in the test rather than an environmental issue.
- jobs: int local rootless debian-sid
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.463 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 09:04 . dr-xr-xr-x 1 root root 100 Aug 12 09:04 .. -rw------- 1 root root 0 Aug 12 09:04 2725100522
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential issue in the test logic or the functionality being tested.
- jobs: int local rootless fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.487 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:55 . dr-xr-xr-x 1 root root 100 Aug 12 06:55 .. -rw------- 1 root root 0 Aug 12 06:55 1481330741
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int remote root debian-sid
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.585 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 07:02 . dr-xr-xr-x 1 root root 100 Aug 12 07:02 .. -rw------- 1 root root 0 Aug 12 07:02 1058525773
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected ownership of the files in the volume did not match the actual ownership, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int local rootless fedora-current
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.598 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:16 . dr-xr-xr-x 1 root root 100 Aug 12 06:16 .. -rw------- 1 root root 0 Aug 12 06:16 3568625069
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the code being tested. The expectation of user IDs '9999 9999' not being present suggests a misconfiguration or error in the test setup.
- jobs: int remote rootless fedora-current
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.685 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:15 . dr-xr-xr-x 1 root root 100 Aug 12 06:15 .. -rw------- 1 root root 0 Aug 12 06:15 2184194914
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int remote root debian-sid
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.701 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:53 . dr-xr-xr-x 1 root root 100 Aug 12 06:53 .. -rw------- 1 root root 0 Aug 12 06:53 2699395562
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int local root fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.709 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:19 . dr-xr-xr-x 1 root root 100 Aug 12 06:19 .. -rw------- 1 root root 0 Aug 12 06:19 131487857
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected ownership of the file did not match the actual ownership, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int local rootless fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.743 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 07:01 . dr-xr-xr-x 1 root root 100 Aug 12 07:01 .. -rw------- 1 root root 0 Aug 12 07:01 1519175452
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the code being tested.
- jobs: int remote root fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.744 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:19 . dr-xr-xr-x 1 root root 100 Aug 12 06:19 .. -rw------- 1 root root 0 Aug 12 06:19 2713908280
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the functionality being tested. The expectation of user IDs in the output suggests a flaw in how the container's volume permissions are being handled.
- jobs: int remote root fedora-current
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.764 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 07:00 . dr-xr-xr-x 1 root root 100 Aug 12 07:00 .. -rw------- 1 root root 0 Aug 12 07:00 1098788442
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential issue in the test logic or the code being tested. The expectation that the output should contain '9999 9999' suggests a bug in the test rather than an environmental issue.
- jobs: int local root debian-sid
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.841 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:13 . dr-xr-xr-x 1 root root 100 Aug 12 06:13 .. -rw------- 1 root root 0 Aug 12 06:13 1062059048
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected ownership of the files in the volume did not match the actual ownership, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int local rootless fedora-current
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [4.923 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:16 . dr-xr-xr-x 1 root root 100 Aug 12 06:16 .. -rw------- 1 root root 0 Aug 12 06:16 2690689185
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential issue in the test logic or the code being tested. The expectation that the output should contain '9999 9999' suggests a bug in the test rather than an environmental issue.
- jobs: int local root debian-sid
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [5.049 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 07:01 . dr-xr-xr-x 1 root root 100 Aug 12 07:01 .. -rw------- 1 root root 0 Aug 12 07:01 3166659166
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int local rootless fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### TEST_TIMEOUT (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [5.066 seconds]`
- evidence: `[FAILED] timed out waiting for "TBAwcJiPXTcusAKkhZZn" in logs of container c-multi-3`
- note: The failure message indicates a timeout while waiting for a specific log output from a container, which is characteristic of a test that exceeds expected execution time.
- jobs: int local rootless fedora-prior
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [5.115 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 09:04 . dr-xr-xr-x 20 root root 400 Aug 12 09:04 .. -rw------- 1 root root 0 Aug 12 09:04 98311648
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int local rootless fedora-prior
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [5.161 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 07:06 . dr-xr-xr-x 20 root root 400 Aug 12 07:06 .. -rw------- 1 root root 0 Aug 12 07:06 53533794
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential issue in the test logic or the code being tested. The expectation that the output should contain '9999 9999' suggests a bug in the test rather than an environmental issue.
- jobs: int local root fedora-prior
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [5.249 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:59 . dr-xr-xr-x 1 root root 100 Aug 12 06:59 .. -rw------- 1 root root 0 Aug 12 06:58 1238969153
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential issue in the test logic or the code being tested. The expectation that the output should contain '9999 9999' suggests a bug in the test rather than an environmental issue.
- jobs: int remote root fedora-current
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [5.251 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:17 . dr-xr-xr-x 20 root root 400 Aug 12 06:17 .. -rw------- 1 root root 0 Aug 12 06:17 699050624
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int local root fedora-prior
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [5.551 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:19 . dr-xr-xr-x 1 root root 100 Aug 12 06:19 .. -rw------- 1 root root 0 Aug 12 06:19 1443419650
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the code being tested. The expectation that the output should contain '9999 9999' suggests a flaw in the test's assumptions.
- jobs: int remote root fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [5.608 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:14 . dr-xr-xr-x 20 root root 400 Aug 12 06:14 .. -rw------- 1 root root 0 Aug 12 06:14 3580032078
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int remote root fedora-prior
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [5.795 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:16 . dr-xr-xr-x 1 root root 100 Aug 12 06:16 .. -rw------- 1 root root 0 Aug 12 06:16 423028925
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int local root fedora-current
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [5.923 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:15 . dr-xr-xr-x 1 root root 100 Aug 12 06:15 .. -rw------- 1 root root 0 Aug 12 06:15 3613670900
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int local root fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [5.959 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 06:59 . dr-xr-xr-x 20 root root 400 Aug 12 06:59 .. -rw------- 1 root root 0 Aug 12 06:59 216420058
  to contain substring
      <string>: 9999 9999`
- note: The test failed because the expected output did not match the actual output, indicating a potential issue in the test logic or the code under test. The expectation that the output should contain '9999 9999' suggests a bug in the handling of user permissions.
- jobs: int remote root fedora-prior
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `Podman pod stop | • [FAILED] [11.272 seconds]`
- evidence: `Unexpected warnings seen on stderr: "time=\"2026-08-13T18:48:10Z\" level=warning msg=\"StopSignal SIGTERM failed to stop container c1931bf2913f-infra in 10 seconds, resorting to SIGKILL\""`
- note: The test failed due to an unexpected warning related to the inability to stop a container within the expected time frame. This indicates a potential bug in the test logic or the Podman pod stop functionality.
- jobs: int local root debian-sid
- seen: 2026-08-13 → 2026-08-13
### TEST_TIMEOUT (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `endable-passta-tests`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman run networking | • [FAILED] [14.080 seconds]`
- evidence: `[FAILED] timed out waiting for "ZQFlmUWVdXMgpHLDCpHc" in logs of container srcip-ctr`
- note: The test failures explicitly state that there was a timeout while waiting for a log output from a container. This indicates that the test did not complete within the expected duration.
- jobs: int local rootless debian-sid
- seen: 2026-08-10 → 2026-08-10
### TEST_TIMEOUT (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `endable-passta-tests`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman run networking | • [FAILED] [14.231 seconds]`
- evidence: `[FAILED] timed out waiting for "OHkumtZLJcFhOkEGpEih" in logs of container srcip-ctr`
- note: The log explicitly states a timeout occurred while waiting for logs from a container, indicating a timing issue during the test execution.
- jobs: int remote rootless fedora-current
- seen: 2026-08-10 → 2026-08-10
### TEST_TIMEOUT (1.00, llm) — 1 occurrence(s) · ⚠ confined to branch `endable-passta-tests`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman run networking | • [FAILED] [14.462 seconds]`
- evidence: `[FAILED] timed out waiting for "FFDCeEEpZSGMOWdOyOIz" in logs of container srcip-ctr`
- note: The failure is directly due to a timeout waiting for specific logs from a running container, indicating that the test did not complete in the expected time frame.
- jobs: int local rootless fedora-current
- seen: 2026-08-10 → 2026-08-10
### TEST_TIMEOUT (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `endable-passta-tests`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman run networking | • [FAILED] [14.474 seconds]`
- evidence: `[FAILED] timed out waiting for "enCMFLBRQcecwNyYoGtR" in logs of container srcip-ctr`
- note: The logs indicate a timeout while waiting for a specific string in the container logs. This pattern is consistent with test timeouts.
- jobs: int local rootless fedora-rawhide
- seen: 2026-08-10 → 2026-08-10
### NETWORK_INFRA (1.00, llm) — 1 occurrence(s) · ⚠ confined to branch `endable-passta-tests`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman run networking | • [FAILED] [14.686 seconds]`
- evidence: `[FAILED] timed out waiting for "QTZPPhvpxQNWdUgAlVTw" in logs of container c-dualip-v6`
- note: The failures indicate timeouts while waiting for specific log messages from the container, suggesting issues with container networking. The tests are specifically related to networking scenarios, pointing to potential network infrastructure problems.
- jobs: int local rootless fedora-prior
- seen: 2026-08-10 → 2026-08-10
### NETWORK_INFRA (1.00, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `Podman run networking | • [FAILED] [2.920 seconds]`
- evidence: `[FAILED] failed to send message to 127.0.0.1:5537 after 1 attempts`
- note: The failure is due to an inability to connect to a local network address, indicating a networking issue. The 'connection refused' error supports the classification under NETWORK_INFRA.
- jobs: int local rootless fedora-rawhide
- seen: 2026-08-11 → 2026-08-11
### NETWORK_INFRA (1.00, llm) — 1 occurrence(s)
- signature: `Podman run networking | • [FAILED] [3.229 seconds]`
- evidence: `[FAILED] failed to send message to 127.0.0.1:5744 after 1 attempts`
- note: The error indicates a failure to connect to a network address, suggesting issues related to the networking infrastructure. The specific mention of 'connection refused' further supports this classification.
- jobs: int local rootless fedora-current
- seen: 2026-08-10 → 2026-08-10
### TEST_TIMEOUT (1.00, llm) — 1 occurrence(s) · ⚠ confined to branch `issue/ci`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman run networking | • [FAILED] [8.912 seconds]`
- evidence: `[FAILED] timed out waiting for "bteDlIaSOPjIGXNIiykX" in logs of container c-multiip-2`
- note: The failure indicates a timeout while waiting for specific logs from the container, which directly suggests a test timeout issue.
- jobs: int local rootless fedora-current
- seen: 2026-08-13 → 2026-08-13
### TEST_TIMEOUT (1.00, llm) — 1 occurrence(s) · ⚠ confined to branch `renovate/github.com-sirupsen-logrus-1.x`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman run networking | • [FAILED] [8.921 seconds]`
- evidence: `[FAILED] timed out waiting for "DFrRSXpCGFQnyPUFAUba" in logs of container c-multi-3`
- note: The test indicates a timeout while waiting for output in the logs of a specific container, which directly points to the test exceeding the expected execution time.
- jobs: int remote rootless fedora-current
- seen: 2026-08-13 → 2026-08-13
### TEST_TIMEOUT (1.00, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `Podman run networking | • [FAILED] [8.973 seconds]`
- evidence: `[FAILED] timed out waiting for "VlvMmqiHkylgiypAsCTV" in logs of container c-multi-2`
- note: The failure indicates that the test timed out while waiting for a specific log entry from the container. This directly supports the classification of a test timeout as the cause of failure.
- jobs: int remote rootless fedora-current
- seen: 2026-08-10 → 2026-08-10
### TEST_TIMEOUT (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `Podman run networking | • [FAILED] [9.469 seconds]`
- evidence: `[FAILED] timed out waiting for "KnNnLyvQVmAEQqZQaJbH" in logs of container c-multi-3`
- note: The failure is explicitly related to timing out while waiting for logs from a container, indicating that the test did not complete in the expected time frame.
- jobs: int local rootless debian-sid
- seen: 2026-08-11 → 2026-08-11
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman run with volumes | • [FAILED] [1.634 seconds]`
- evidence: `[FAILED] Expected
      <string>: 1777 1786525695
  to equal
      <string>: 1777 1566297043`
- note: The test is failing due to an unexpected value being returned, indicating a potential bug in the test logic or the product's handling of volume permissions.
- jobs: int remote root fedora-prior
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman run with volumes | • [FAILED] [1.688 seconds]`
- evidence: `[FAILED] Expected
      <string>: 1777 1786525417
  to equal
      <string>: 1777 1566297043`
- note: The test is failing due to an unexpected value being returned, indicating a potential bug in the test logic or the product's handling of volume permissions.
- jobs: int remote root fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix-kube-seccomp-profile`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman run with volumes | • [FAILED] [1.862 seconds]`
- evidence: `[FAILED] Expected
      <string>: arch keys protected_paths.d repositories world
  to equal
      <string>: arch`
- note: The test failed because the expected output did not match the actual output, indicating a potential bug in the test logic or the functionality being tested.
- jobs: int local root debian-sid
- seen: 2026-08-13 → 2026-08-13
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman run with volumes | • [FAILED] [1.890 seconds]`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 09:04 . dr-xr-xr-x 1 root root 100 Aug 12 09:04 .. -rw------- 1 root root 0 Aug 12 09:04 4152098143
  to contain substring
      <string>: 9999 9999
  In [It] at: /var/tmp/podman-container-tools/podman/test/e2e/cp_test.go:287 @ 08/12/26 09:04:37.809`
- note: The test is failing because it expects a specific user ID and group ID (9999) to be present in the output, but it is not found. This indicates a potential bug in the test logic or the functionality being tested.
- jobs: int remote root fedora-current
- seen: 2026-08-12 → 2026-08-12
### PRODUCT_RACE (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman run | • [FAILED] [1.657 seconds]`
- evidence: `[FAILED] Expected
      <string>: 1777 1786525565
  to equal
      <string>: 1777 1566297043`
- note: The test failures indicate a race condition where the expected permissions of a volume are not being honored, leading to inconsistent results. This suggests a potential issue with how Podman handles volume permissions across different runs.
- jobs: int remote root debian-sid
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix-secret-event-filter`, never re-run to green — likely that PR's regression, not a flake
- signature: ``events.Secret` is a core event type defined in `libpod/events/config.go`, and secret operations record events with `e.Type = events.Secret`. However, `generateEventFilter` previously lacked a `case "SECRET":` block, causing `podman events --filter secret=<name>` to fail with `Error: SECRET is an invalid filter`.`
- evidence: `causing `podman events --filter secret=<name>` to fail with `Error: SECRET is an invalid filter`.`
- note: The failure is due to a missing case in the event filter handling, which indicates a bug in the test logic related to filtering events. This suggests that the test is not functioning as intended because it relies on a feature that was not implemented correctly.
- jobs: Validate source code changes
- seen: 2026-08-11 → 2026-08-11
### NETWORK_INFRA (1.00, regex) — 1 occurrence(s) · ⚠ confined to branch `fix-swagger-warnings`, never re-run to green — likely that PR's regression, not a flake
- signature: `curl: (7) Failed to connect to localhost port 80 after 0 ms: Couldn't connect to server`
- evidence: `curl: (7) Failed to connect to localhost port 80 after 0 ms: Couldn't connect to server`
- note: curl failure fetching an external resource
- jobs: int remote rootless fedora-current
- seen: 2026-08-04 → 2026-08-04
### TEST_BUG (0.80, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `not ok N |030| podman run docker-archive in DUR | # `run_podman create docker-archive:$archive' failed`
- evidence: ``run_podman create docker-archive:$archive' failed`
- note: The failure indicates a specific issue with the podman run command failing to create a docker-archive, which suggests a bug in the test itself rather than an infrastructure issue.
- jobs: sys local root fedora-current
- seen: 2026-08-12 → 2026-08-12
### PARALLEL_INTERFERENCE (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `not ok N |065| podman cp file from container to container in DUR | # `basic_teardown' failed`
- evidence: `not ok 127 |065| podman cp file from container to container in 64196ms`
- note: The test failure occurs in a parallel context, which suggests interference between tests. The unusually high duration for the operation may indicate contention for resources.
- jobs: sys local root fedora-rawhide
- seen: 2026-08-04 → 2026-08-04
### UNKNOWN (0.00, llm) — 1 occurrence(s)
- signature: `not ok N |125| podman import in DUR | # `run_podman import -q $archive' failed`
- evidence: `not ok 174 |125| podman import in 2137ms`
- note: The log indicates a failure with 'podman import', but it does not provide explicit details on the underlying cause. Therefore, it's uncertain what specific category this failure belongs to.
- jobs: sys remote rootless fedora-current
- seen: 2026-08-06 → 2026-08-06
### TEST_TIMEOUT (0.90, llm) — 1 occurrence(s)
- signature: `not ok N |220| podman healthcheck in DUR | # `_check_health $ctrname "First failure" "' failed`
- evidence: `#| FAIL: First failure - timed out waiting for 'healthy' in podman events`
- note: The failure suggests that the test encountered a timeout while waiting for a specific condition to be met, indicating a test did not complete in the expected time frame.
- jobs: sys local rootless fedora-current
- seen: 2026-08-09 → 2026-08-09
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/machine-image-permissions`, never re-run to green — likely that PR's regression, not a flake
- signature: `not ok N |220| podman healthcheck in DUR | # `cidmatch=$(grep "$cid" <<<"$output")' failed`
- evidence: `#| expected: '"healthy"'`
- note: The test expected the health status to be 'healthy', but it received 'unhealthy', indicating a failure in the test logic or the health check implementation.
- jobs: sys local rootless fedora-prior
- seen: 2026-08-08 → 2026-08-08
### UNKNOWN (0.00, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `not ok N |252| quadlet - image tag in DUR | # `service_setup $container_service' failed`
- evidence: `not ok 271 |252| quadlet - image tag in 5987ms`
- note: The log indicates a failure during the 'quadlet - image tag' test, but there is insufficient detail to determine the specific cause of the failure.
- jobs: sys local rootless fedora-current
- seen: 2026-08-07 → 2026-08-07
### HARNESS (0.90, llm) — 1 occurrence(s)
- signature: `not ok N |450| podman detects correct tty size in DUR | # `is "$output" "$rows $cols$CR" "stty under podman exec reads the correct dimensions"' failed`
- evidence: `not ok 317 |450| podman detects correct tty size in 4213ms`
- note: The failure indicates that the test related to detecting the correct TTY size did not succeed. This suggests an issue with the harness or the way the test is set up rather than a problem with the Podman product itself.
- jobs: sys local rootless debian-sid
- seen: 2026-08-09 → 2026-08-09
### NETWORK_INFRA (1.00, llm) — 1 occurrence(s) · ⚠ confined to branch `renovate/golang.org-x-net-0.x`, never re-run to green — likely that PR's regression, not a flake
- signature: `not ok N |505| UDP/IPv6 large transfer, tap in DUR | # `pasta_test_do' failed`
- evidence: `#|     FAIL: Mismatch between data sent and received`
- note: The failure involves a mismatch in data sizes and a UDP-based transfer, indicating a potential problem with network communication. This aligns with issues typically categorized under network infrastructure problems.
- jobs: sys local rootless debian-sid
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s)
- signature: `not ok N |700| podman play with user from image in DUR | # `run_podman build --layers=false --unsetenv PATH -t $imgname $PODMAN_TMPDIR' failed`
- evidence: ``run_podman build --layers=false --unsetenv PATH -t $imgname $PODMAN_TMPDIR' failed`
- note: The failure indicates that the `run_podman` command did not complete successfully, suggesting a potential issue with the test itself rather than a systemic problem.
- jobs: sys local root fedora-prior
- seen: 2026-08-13 → 2026-08-13
### TEST_BUG (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `time="DATETTIMEZ" level=error msg="unlinkat /tmp/podman-e2e-X directory not empty"`
- evidence: `Unexpected warnings seen on stderr: "time=\"2026-08-10T13:05:03Z\" level=error msg=\"unlinkat /tmp/podman-e2e-2701650693/subtest-1777352725/p/clitmp/events: directory not empty\""`
- note: The failure indicates a test-related issue where the system reset function does not behave as expected, leading to an error about a non-empty directory. This suggests a bug within the test or the functionality being tested.
- jobs: int local root fedora-current
- seen: 2026-08-10 → 2026-08-10
## Top re-run-confirmed flaky jobs
- 6× `Validate source code changes`
- 5× `sys local root fedora-rawhide`
- 4× `windows installer wsl`
- 3× `macos machine libkrun`
- 3× `int remote rootless fedora-current`
- 2× `windows installer hyperv`
- 2× `sys local rootless fedora-current`
- 2× `sys local rootless debian-sid`
- 2× `int local rootless fedora-prior`
- 2× `int local rootless fedora-current`
