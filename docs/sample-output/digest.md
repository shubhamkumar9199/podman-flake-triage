# Podman CI flake digest — 2026-08-15
Window: 2026-08-04T00:49:41Z → 2026-08-13T21:00:13Z · workflow `ci.yml` · repo `podman-container-tools/podman`
## Volume
- runs analyzed (completed, non-`action_required`): **174**
- runs needing >1 attempt: **64** (37%)
- confirmed flakes (job FAIL→PASS at identical commit): **62**
> Detection is attempt-diff based (`/jobs?filter=all`). A `?status=failure`
> listing cannot see re-run-to-green runs at all, and a green re-run alone is
> treated as *observation*, not proof — classification comes from log evidence.
## Failure clusters
### TEST_BUG (0.90, llm) — 37 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `not ok N |065| podman cp file from host to container volume in DUR | # `is "$output" ""' failed`
- evidence: `#|     FAIL: podman cp /tmp/podman_bats.LV9tPd/cp-test-volume/hostfile c-cp_t132-scnkbc3k:/tmp/volume/sub-volume
#| expected: '[no output]'
#|   actual: 'sub-volume'
#\^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^`
- note: The failure indicates that the expected output from the 'podman cp' command did not match the actual output, suggesting a potential bug in the test or the command itself.
- jobs: sys local root debian-sid,sys remote root fedora-rawhide,sys local rootless fedora-current,sys local root fedora-rawhide,sys remote rootless fedora-current,sys remote root fedora-current,sys local rootless fedora-prior,sys local root fedora-prior,sys remote root fedora-prior,sys remote root debian-sid,sys local rootless fedora-rawhide,sys local root fedora-current,sys local rootless debian-sid
- seen: 2026-08-12 → 2026-08-12
### TEST_TIMEOUT (0.90, llm) — 31 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman cp | • [FAILED] [DUR]`
- evidence: `[FAILED] timed out waiting for "TBAwcJiPXTcusAKkhZZn" in logs of container c-multi-3`
- note: The failure indicates a timeout while waiting for specific logs from a container, which is characteristic of a test timeout issue.
- jobs: int remote rootless fedora-current,int local rootless fedora-prior,int remote root fedora-prior,int local root debian-sid,int local root fedora-current,int local rootless fedora-current,int remote root fedora-rawhide,int remote root fedora-current,int local rootless fedora-rawhide,int local rootless debian-sid,int remote root debian-sid,int local root fedora-rawhide,int local root fedora-prior
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
### TEST_TIMEOUT (0.90, llm) — 11 occurrence(s) · 3 re-run-confirmed
- signature: `Podman run networking | • [FAILED] [DUR]`
- evidence: `[FAILED] timed out waiting for "OHkumtZLJcFhOkEGpEih" in logs of container srcip-ctr`
- note: The logs indicate that the test failed due to a timeout while waiting for specific logs from a container. This suggests that the failure is related to a timeout issue during the test execution.
- jobs: int local rootless fedora-current,int remote rootless fedora-current,int local rootless fedora-prior,int local rootless debian-sid,int local rootless fedora-rawhide
- seen: 2026-08-10 → 2026-08-13
### NETWORK_INFRA (1.00, regex) — 10 occurrence(s) · 7 re-run-confirmed
- signature: `curl: (56) Connection died, tried 5 times before giving up`
- evidence: `curl: (56) Connection died, tried 5 times before giving up`
- note: connection died mid-transfer
- jobs: build fedora-current,build fedora-rawhide,build debian-sid,int local rootless fedora-current,int local root fedora-rawhide,bud local root fedora-current,int remote root debian-sid,sys remote root fedora-prior,int local rootless debian-sid
- seen: 2026-08-12 → 2026-08-12
### VM_INFRA (0.90, llm) — 8 occurrence(s)
- signature: `Error: building at STEP "RUN ip addr": opening seccomp profile failed: open /etc/containers/seccomp.json: no such file or directory`
- evidence: `Error: building at STEP "RUN ip addr": opening seccomp profile failed: open /etc/containers/seccomp.json: no such file or directory`
- note: The error indicates a failure related to the virtual machine infrastructure, specifically the absence of a required seccomp profile file. This suggests an issue with the VM environment setup.
- jobs: machine linux amd64
- seen: 2026-08-11 → 2026-08-13
### TEST_BUG (0.90, llm) — 5 occurrence(s) · 1 re-run-confirmed
- signature: `not ok N |220| podman healthcheck in DUR | # `assert "$output" =~ "StartLimitIntervalUSec=0" "The hc service has the right interval set"' failed`
- evidence: `#   `assert "$output" =~ "StartLimitIntervalUSec=0" "The hc service has the right interval set"' failed`
- note: The failure indicates that an assertion related to the health check service's configuration did not pass, suggesting a potential bug in the test or the health check implementation itself.
- jobs: sys remote root fedora-current,sys local rootless debian-sid,sys local root debian-sid,sys remote root fedora-rawhide,sys local rootless fedora-current
- seen: 2026-08-13 → 2026-08-13
### NETWORK_INFRA (1.00, regex) — 5 occurrence(s) · 3 re-run-confirmed
- signature: `curl: (6) Could not resolve host: www.redhat.com`
- evidence: `curl: (6) Could not resolve host: www.redhat.com`
- note: curl failure fetching an external resource
- jobs: int local root fedora-rawhide,int remote rootless fedora-current,int local rootless fedora-current,int local root fedora-prior,int remote root fedora-prior
- seen: 2026-08-04 → 2026-08-12
### TEST_TIMEOUT (1.00, regex) — 5 occurrence(s)
- signature: `[TIMEDOUT] A suite timeout occurred`
- evidence: `[TIMEDOUT] A suite timeout occurred`
- note: suite deadline expired; the named spec is whichever was in flight, not the culprit
- jobs: windows machine hyperv
- seen: 2026-08-05 → 2026-08-13
### TEST_BUG (0.90, llm) — 4 occurrence(s) · ⚠ confined to branch `fix-25362-config-log-level`, never re-run to green — likely that PR's regression, not a flake
- signature: `not ok N [800] podman --module - command-line completion in DUR | # `assert "${lines[0]}" = "--module=" "completion ignores the incomplete early flag"' failed`
- evidence: `#|     FAIL: completion ignores the incomplete early flag
#| expected: = --module=
#|   actual:   --module`
- note: The failure indicates that the command-line completion is not functioning as expected, which suggests a bug in the test itself rather than an issue with the environment or infrastructure.
- jobs: sys local rootless fedora-current,sys local rootless debian-sid,sys local rootless fedora-prior,sys local rootless fedora-rawhide
- seen: 2026-08-10 → 2026-08-10
### NETWORK_INFRA (1.00, regex) — 4 occurrence(s) · 2 re-run-confirmed
- signature: `curl: (52) Empty reply from server`
- evidence: `curl: (52) Empty reply from server`
- note: curl failure fetching an external resource
- jobs: windows installer wsl,windows machine wsl
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 4 occurrence(s)
- signature: `Podman run with volumes | • [FAILED] [DUR]`
- evidence: `[FAILED] Expected
      <string>: 1777 1786525417
  to equal
      <string>: 1777 1566297043
  In [It] at: /var/tmp/podman-container-tools/podman/test/e2e/run_test.go:1150 @ 08/12/26 09:03:41.709`
- note: The test is failing due to an unexpected value being returned, indicating a potential bug in the test logic or the product behavior. The failure is consistent across multiple test cases related to volume permissions.
- jobs: int remote root fedora-prior,int remote root fedora-current,int remote root fedora-rawhide,int local root debian-sid
- seen: 2026-08-12 → 2026-08-13
### VM_INFRA (0.90, llm) — 3 occurrence(s)
- signature: `Error: machine did not transition into running state: ssh error: ssh: handshake failed: read tcp 127.0.0.1:NUM->127.0.0.1:NUM: wsarecv: An existing connection was forcibly closed by the remote host.`
- evidence: `Error: machine did not transition into running state: ssh error: ssh: handshake failed: read tcp 127.0.0.1:51788->127.0.0.1:51692: wsarecv: An existing connection was forcibly closed by the remote host.`
- note: The failure is related to the virtual machine not transitioning to a running state due to an SSH handshake failure, indicating an issue with the VM infrastructure.
- jobs: windows machine hyperv
- seen: 2026-08-06 → 2026-08-13
### UNKNOWN (0.00, llm) — 3 occurrence(s) · 1 re-run-confirmed
- signature: `# Error: copying layers and metadata for container "HEX": writing blob: adding layer with blob "sha256:HEX"/""/"sha256:HEX": unpacking failed (error: exit status 1; output: mkdir /run: no such file or directory)`
- jobs: sys local root fedora-rawhide,sys local root debian-sid
- seen: 2026-08-09 → 2026-08-13
### TEST_TIMEOUT (0.90, llm) — 2 occurrence(s)
- signature: `not ok N bud-github-context-with-branch-subdir-commit | # `run_buildah build $WITH_POLICY_JSON -t ${target} "${gitrepo}"' failed`
- evidence: `*** TIMED OUT ***`
- note: The log explicitly indicates a timeout with the message '*** TIMED OUT ***', suggesting that the test did not complete within the expected time frame.
- jobs: bud local root fedora-current,bud remote root fedora-current
- seen: 2026-08-12 → 2026-08-12
### UNKNOWN (0.00, llm) — 2 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `not ok N [23-containersArchive] POST exec/HEX/start [-d {}] : output`
- jobs: apiv2  root fedora-current,apiv2  rootless fedora-current
- seen: 2026-08-07 → 2026-08-07
### TEST_TIMEOUT (1.00, llm) — 2 occurrence(s)
- signature: `Error: ssh: handshake failed: read tcp 127.0.0.1:NUM->127.0.0.1:NUM: wsarecv: An existing connection was forcibly closed by the remote host.`
- evidence: `[TIMEDOUT] podman machine start [It] start simple machine
  D:/a/podman/podman/pkg/machine/e2e/start_test.go:18`
- note: The log indicates a timeout occurred during the execution of the test case 'start simple machine', which directly points to a test timeout failure.
- jobs: windows machine hyperv
- seen: 2026-08-11 → 2026-08-13
### VM_INFRA (0.90, llm) — 2 occurrence(s) · 1 re-run-confirmed
- signature: `Error: machine did not transition into running state: ssh error: ssh: handshake failed: read tcp 127.0.0.1:NUM->127.0.0.1:NUM: read: connection reset by peer`
- evidence: `Error: machine did not transition into running state: ssh error: ssh: handshake failed: read tcp 127.0.0.1:64180->127.0.0.1:64153: read: connection reset by peer`
- note: The error indicates a failure in establishing an SSH connection to the virtual machine, suggesting an issue with the VM infrastructure.
- jobs: macos machine libkrun
- seen: 2026-08-11 → 2026-08-13
### VM_INFRA (0.90, llm) — 2 occurrence(s) · 1 re-run-confirmed
- signature: `Error: machine did not transition into running state: ssh error: machine not in running state`
- evidence: `Error: machine did not transition into running state: ssh error: machine not in running state`
- note: The failure indicates that the virtual machine did not start properly, which is a clear issue with the VM infrastructure. The specific error message about the machine not being in a running state supports this classification.
- jobs: windows machine wsl
- seen: 2026-08-06 → 2026-08-13
### UNKNOWN (0.00, llm) — 2 occurrence(s)
- signature: `Error: failed to remove machines files: remove C:\Users\RUNNER~1\AppData\Local\Temp\podman_test2722611864\.local\share\containers\podman\machine\hyperv\HEX-amd64.vhdx: The process cannot access the file because it is being used by another process.`
- jobs: windows machine hyperv
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 2 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Error: crun: (00.NUM) Error (criu/cgroup.c:NUM): cg: cgroupd: recv req error: No such file or directory: OCI runtime attempted to invoke a command that was not found`
- evidence: `[FAILED] Expected
      <string>: total 0 drwxr-xr-x 2 root root 60 Aug 12 09:02 . dr-xr-xr-x 1 root root 100 Aug 12 09:02 .. -rw------- 1 root root 0 Aug 12 09:02 419713735
  to contain substring
      <string>: 9999 9999`
- note: The test failure indicates that the expected ownership of the files in the volume does not match the actual ownership, suggesting a bug in the uid/gid mapping logic of the Podman implementation.
- jobs: int local root debian-sid,int local root fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 2 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Error: `/usr/bin/crun checkpoint --image-path /tmp/podman-e2e-X --work-path /tmp/podman-e2e-X HEX` failed: exit status 1`
- evidence: `[FAILED] Expected
      <string>: 1777 1786525282
  to equal
      <string>: 1777 1566297043`
- note: The test failure indicates an unexpected value comparison, suggesting a potential bug in the test logic or the product's handling of named volumes.
- jobs: int local root fedora-current,int local root fedora-prior
- seen: 2026-08-12 → 2026-08-12
### PRODUCT_RACE (0.90, llm) — 2 occurrence(s)
- signature: `# Error: retrieving label for image "HEX": you may need to remove the image to resolve the error: fallback error checking whether image is a manifest list: choosing image instance: no image found in manifest list for architecture "amd64", variant "", OS "linux": choosing image instance: no image found in manifest list for architecture "amd64", variant "", OS "linux"`
- evidence: `# Error: retrieving label for image "3866529f8180390e95c2c550029114a2b3f86ccc9986508b3df1e33b7ef12a66": you may need to remove the image to resolve the error: fallback error checking whether image is a manifest list: choosing image instance: no image found in manifest list for architecture "amd64", variant "", OS "linux": choosing image instance: no image found in manifest list for architecture "amd64", variant "", OS "linux"`
- note: The error indicates that the image retrieval failed due to a missing image in the manifest list, which suggests a race condition in image availability. This aligns with the characteristics of a product race failure.
- jobs: sys remote rootless fedora-current,sys remote root fedora-prior
- seen: 2026-08-11 → 2026-08-12
### PRODUCT_RACE (0.90, llm) — 2 occurrence(s)
- signature: `# Error: copying layers and metadata for container "HEX": committing the finished image: creating image "HEX": layer not known`
- evidence: `# Error: copying layers and metadata for container "10c0892a5bd08954b21cff001d223e1dc78a09b4f159df132ab22e497c73695a": committing the finished image: creating image "fcbdcb271e5e194ec13410884753fdc9bad59a23d1853299fbf33e5f8f34ba59": layer not known`
- note: The error indicates that the image layer is not known, which suggests a potential race condition in the image creation process. This aligns with the characteristics of a product race failure.
- jobs: sys remote root debian-sid,sys local rootless fedora-current
- seen: 2026-08-13 → 2026-08-13
### NETWORK_INFRA (1.00, llm) — 2 occurrence(s) · 1 re-run-confirmed
- signature: `# Error: cannot bind tcp port :NUM: address already in use`
- evidence: `# Error: cannot bind tcp port :5113: address already in use`
- note: The failure is related to a network operation where a TCP port is already in use, indicating a network infrastructure issue.
- jobs: sys local root debian-sid,sys local root fedora-rawhide
- seen: 2026-08-10 → 2026-08-10
### NETWORK_INFRA (1.00, llm) — 2 occurrence(s)
- signature: `# Error: cannot bind tcp port 127.0.0.1:NUM: address already in use`
- evidence: `Error: cannot bind tcp port 127.0.0.1:5400: address already in use`
- note: The failure is due to an inability to bind to a TCP port, indicating a network-related issue. This suggests a problem with network infrastructure rather than a bug in the test or product.
- jobs: sys remote root fedora-rawhide,sys local root fedora-rawhide
- seen: 2026-08-11 → 2026-08-11
### TEST_BUG (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `time="DATETTIMEZ" level=error msg="unlinkat /tmp/podman-e2e-X directory not empty"`
- evidence: `Unexpected warnings seen on stderr: "time=\"2026-08-10T13:05:03Z\" level=error msg=\"unlinkat /tmp/podman-e2e-2701650693/subtest-1777352725/p/clitmp/events: directory not empty\""`
- note: The failure indicates an unexpected error related to a directory not being empty during a system reset operation, suggesting a potential bug in the test or the functionality being tested.
- jobs: int local root fedora-current
- seen: 2026-08-10 → 2026-08-10
### TEST_BUG (0.90, llm) — 1 occurrence(s)
- signature: `not ok N |700| podman play with user from image in DUR | # `run_podman build --layers=false --unsetenv PATH -t $imgname $PODMAN_TMPDIR' failed`
- evidence: `#   `run_podman build --layers=false --unsetenv PATH -t $imgname $PODMAN_TMPDIR' failed`
- note: The failure indicates that a command related to building an image failed, which suggests a potential issue in the test logic or setup rather than an environmental problem.
- jobs: sys local root fedora-prior
- seen: 2026-08-13 → 2026-08-13
### NETWORK_INFRA (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `renovate/golang.org-x-net-0.x`, never re-run to green — likely that PR's regression, not a flake
- signature: `not ok N |505| UDP/IPv6 large transfer, tap in DUR | # `pasta_test_do' failed`
- evidence: `#|     FAIL: Mismatch between data sent and received
#| expected: = size=53248 hash=bb3bee0b2eb44fa3830eadd6b3cd48d8 - head= a9 0a da 48 2a af 08 16 tail= e2 bb 90 31 e7 7c 91 28
#|   actual:   size=49152 hash=1ac838d259ddceda8d151d8ad4faadce - head= a9 0a da 48 2a af 08 16 tail= 3f 77 ca de c5 f8 72 bf`
- note: The failure indicates a mismatch between the expected and actual data sizes during a network transfer, suggesting a network-related issue. This aligns with the category of NETWORK_INFRA.
- jobs: sys local rootless debian-sid
- seen: 2026-08-12 → 2026-08-12
### UNKNOWN (0.00, llm) — 1 occurrence(s)
- signature: `not ok N |450| podman detects correct tty size in DUR | # `is "$output" "$rows $cols$CR" "stty under podman exec reads the correct dimensions"' failed`
- jobs: sys local rootless debian-sid
- seen: 2026-08-09 → 2026-08-09
### TEST_BUG (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `not ok N |252| quadlet - image tag in DUR | # `service_setup $container_service' failed`
- evidence: `#   `service_setup $container_service' failed`
- note: The failure indicates that the service setup for the container could not be completed, which suggests a bug in the test setup or execution. This is not related to infrastructure or timeouts, but rather an issue with the test itself.
- jobs: sys local rootless fedora-current
- seen: 2026-08-07 → 2026-08-07
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/machine-image-permissions`, never re-run to green — likely that PR's regression, not a flake
- signature: `not ok N |220| podman healthcheck in DUR | # `cidmatch=$(grep "$cid" <<<"$output")' failed`
- evidence: `#| expected: '"healthy"'
#|   actual: '"unhealthy"'`
- note: The test expected the health check status to be 'healthy', but it received 'unhealthy', indicating a failure in the test logic or the health check implementation.
- jobs: sys local rootless fedora-prior
- seen: 2026-08-08 → 2026-08-08
### TEST_TIMEOUT (0.90, llm) — 1 occurrence(s)
- signature: `not ok N |220| podman healthcheck in DUR | # `_check_health $ctrname "First failure" "' failed`
- evidence: `#| FAIL: First failure - timed out waiting for 'healthy' in podman events`
- note: The log indicates a failure due to a timeout while waiting for a health check to report 'healthy'. This directly supports the classification of a test timeout.
- jobs: sys local rootless fedora-current
- seen: 2026-08-09 → 2026-08-09
### TEST_BUG (0.90, llm) — 1 occurrence(s)
- signature: `not ok N |125| podman import in DUR | # `run_podman import -q $archive' failed`
- evidence: `#   `run_podman import -q $archive' failed`
- note: The failure indicates that the `podman import` command did not execute successfully, suggesting a potential issue with the test itself rather than an environmental problem.
- jobs: sys remote rootless fedora-current
- seen: 2026-08-06 → 2026-08-06
### PARALLEL_INTERFERENCE (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `not ok N |065| podman cp file from container to container in DUR`
- evidence: `# tags: ci:parallel`
- note: The presence of the 'ci:parallel' tag suggests that the test may be affected by interference from other parallel tests. This indicates a potential issue with test isolation in a parallel execution environment.
- jobs: sys local root fedora-rawhide
- seen: 2026-08-04 → 2026-08-04
### PARALLEL_INTERFERENCE (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `not ok N |030| podman run docker-archive in DUR | # `run_podman create docker-archive:$archive' failed`
- evidence: `not ok 21 |030| podman run docker-archive in 6571ms`
- note: The failure occurred during a parallel execution context, which suggests that interference from other tests may have impacted the outcome. The specific failure message indicates a problem with running a podman command, which can be influenced by concurrent operations.
- jobs: sys local root fedora-current
- seen: 2026-08-12 → 2026-08-12
### NETWORK_INFRA (1.00, regex) — 1 occurrence(s) · ⚠ confined to branch `fix-swagger-warnings`, never re-run to green — likely that PR's regression, not a flake
- signature: `curl: (7) Failed to connect to localhost port 80 after 0 ms: Couldn't connect to server`
- evidence: `curl: (7) Failed to connect to localhost port 80 after 0 ms: Couldn't connect to server`
- note: curl failure fetching an external resource
- jobs: int remote rootless fedora-current
- seen: 2026-08-04 → 2026-08-04
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix-secret-event-filter`, never re-run to green — likely that PR's regression, not a flake
- signature: ``events.Secret` is a core event type defined in `libpod/events/config.go`, and secret operations record events with `e.Type = events.Secret`. However, `generateEventFilter` previously lacked a `case "SECRET":` block, causing `podman events --filter secret=<name>` to fail with `Error: SECRET is an invalid filter`.`
- evidence: `causing `podman events --filter secret=<name>` to fail with `Error: SECRET is an invalid filter`.`
- note: The failure is due to a missing case in the event filter implementation, which indicates a bug in the test logic related to filtering events.
- jobs: Validate source code changes
- seen: 2026-08-11 → 2026-08-11
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/archive-put-volume-resolution-21861`, never re-run to green — likely that PR's regression, not a flake
- signature: `Podman run | • [FAILED] [DUR]`
- evidence: `[FAILED] Expected
      <string>: 1777 1786525565
  to equal
      <string>: 1777 1566297043
  In [It] at: /var/tmp/podman-container-tools/podman/test/e2e/run_volume_test.go:927 @ 08/12/26 09:06:07.169`
- note: The test is failing due to an unexpected value for permissions, indicating a potential bug in the test logic or the product's handling of volume permissions.
- jobs: int remote root debian-sid
- seen: 2026-08-12 → 2026-08-12
### TEST_BUG (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `Podman pod stop | • [FAILED] [DUR]`
- evidence: `Unexpected warnings seen on stderr: "time=\"2026-08-13T18:48:10Z\" level=warning msg=\"StopSignal SIGTERM failed to stop container c1931bf2913f-infra in 10 seconds, resorting to SIGKILL\""`
- note: The failure is due to a warning indicating that the stop signal failed to terminate a container in the expected time, suggesting a potential issue in the test logic or the handling of container stop signals.
- jobs: int local root debian-sid
- seen: 2026-08-13 → 2026-08-13
### TEST_TIMEOUT (1.00, llm) — 1 occurrence(s) · ⚠ confined to branch `fix/hyperv-vsock-ready-timeout`, never re-run to green — likely that PR's regression, not a flake
- signature: `Error: unsupported provider "wsl"`
- evidence: `[FAILED] Timed out after 600.000s.`
- note: The log indicates a timeout failure after a specified duration, which directly points to a test timeout issue.
- jobs: macos machine applehv
- seen: 2026-08-12 → 2026-08-12
### VM_INFRA (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `Error: unable to start "m2-HEX": m1-HEX already starting or running: only one VM can be active at a time`
- evidence: `Error: unable to start "m2-b9a25a28f240": m1-7a530e072381 already starting or running: only one VM can be active at a time`
- note: The error indicates a conflict in starting multiple virtual machines simultaneously, which is a clear issue related to VM infrastructure.
- jobs: macos machine libkrun
- seen: 2026-08-10 → 2026-08-10
### TEST_TIMEOUT (0.90, llm) — 1 occurrence(s)
- signature: `Error: unable to copy from source docker://quay.io/libpod/testimage:NUM: copying system image from manifest list: parsing image configuration: Get "https://cdn01.quay.io/quayio-production-s3/sha256/b8/HEX?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIATAAF2YHTGR23ZTE6%2F20260805%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260805T100727Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Signature=HEX&region=us-east-1&namespace=libpod&repo_name=testimage&akamai_signature=exp=NUM~hmac=HEX": remote error: tls: internal error`
- evidence: `[TIMEDOUT] podman machine list [It] list machine: check if running while starting
  D:/a/podman/podman/pkg/machine/e2e/list_test.go:71`
- note: The log indicates a timeout occurred during the execution of a test case, specifically when checking if a machine was running while starting. This suggests that the failure is related to a test timing out rather than an issue with the underlying infrastructure.
- jobs: windows machine hyperv
- seen: 2026-08-05 → 2026-08-05
### NETWORK_INFRA (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `Error: pasta failed with exit code 1:`
- evidence: `Listen failed for HOST TCP port */39951: Address already in use`
- note: The failure is due to a port conflict, indicating that the network infrastructure is unable to allocate the requested port for the Podman container.
- jobs: int local rootless fedora-prior
- seen: 2026-08-11 → 2026-08-11
### VM_INFRA (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `renovate/github.com-sirupsen-logrus-1.x`, never re-run to green — likely that PR's regression, not a flake
- signature: `Error: machine did not transition into running state: ssh error: machine is not listening on ssh port`
- evidence: `Error: machine did not transition into running state: ssh error: machine is not listening on ssh port`
- note: The error indicates a failure related to the virtual machine not being able to start due to SSH connectivity issues, which falls under VM infrastructure problems.
- jobs: windows machine wsl
- seen: 2026-08-13 → 2026-08-13
### VM_INFRA (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `Error: krunkit exited unexpectedly with exit code 1`
- evidence: `Error: krunkit exited unexpectedly with exit code 1`
- note: The failure is related to the virtual machine infrastructure, specifically the unexpected exit of the krunkit process, which is responsible for managing the VM environment.
- jobs: macos machine libkrun
- seen: 2026-08-12 → 2026-08-12
### NETWORK_INFRA (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `renovate/golang.org-x-net-0.x`, never re-run to green — likely that PR's regression, not a flake
- signature: `Error: downloading URL "archive": invalid response status 503`
- evidence: `Error: downloading URL "archive": invalid response status 503`
- note: The failure is due to an invalid response status (503) when attempting to download a URL, indicating a network-related issue.
- jobs: int remote root fedora-prior
- seen: 2026-08-12 → 2026-08-12
### PARALLEL_INTERFERENCE (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `Error: committing container for step {Env:[PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin] Command:run Args:[touch rmtest:0] Flags:[] Attrs:map[] Message:RUN touch rmtest:0 Heredocs:[] Original:RUN touch rmtest:0}: copying layers and metadata for container "HEX": writing blob: adding layer with blob "sha256:HEX"/""/"sha256:HEX": unpacking failed (error: exit status 1; output: open /rmtest:0: no such file or directory)`
- evidence: `Error: committing container for step {Env:[PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin] Command:run Args:[touch rmtest:0] Flags:[] Attrs:map[] Message:RUN touch rmtest:0 Heredocs:[] Original:RUN touch rmtest:0}: copying layers and metadata for container "04c35a389d8291aca95228f3ec9f1fd9d671f2b7e963f60973aaaa1690fb2315": writing blob: adding layer with blob "sha256:724a7a770a18a396d836f1d9f138d4d59bc7ccbdcdb52e537e092b917934fa7b"/""/"sha256:58b0aee591ec4897a5508c869395001c63a3e009a77616e68259c57d01af47ad": unpacking failed (error: exit status 1; output: open /rmtest:0: no such file or directory)`
- note: The failure occurred during concurrent operations involving shared layers, leading to a conflict when trying to access a file that does not exist. This suggests that parallel execution of tests is interfering with each other.
- jobs: int local root fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### TEST_TIMEOUT (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `bump-6.1.1-dev`, never re-run to green — likely that PR's regression, not a flake
- signature: `Error: Post "http://localhost:PORT/vm/state": EOF`
- evidence: `[FAILED] Timed out after 600.001s.`
- note: The log indicates a timeout occurred after 600 seconds while waiting for a command to complete, which directly points to a test timeout issue.
- jobs: macos machine applehv
- seen: 2026-08-12 → 2026-08-12
### VM_INFRA (0.90, llm) — 1 occurrence(s)
- signature: `Error: EOF`
- evidence: `Error: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ: VM does not exist`
- note: The failure indicates that a virtual machine (VM) could not be started because it does not exist, which points to an issue with the VM infrastructure.
- jobs: macos machine applehv
- seen: 2026-08-12 → 2026-08-12
### RUNNER_INFRA (1.00, regex) — 1 occurrence(s)
- signature: `##[error]Failed to run: Error: socket hang up, Error: socket hang up`
- evidence: `##[error]Failed to run: Error: socket hang up, Error: socket hang up`
- note: runner provisioning/communication failure
- jobs: Validate source code changes
- seen: 2026-08-12 → 2026-08-12
### RUNNER_INFRA (1.00, regex) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `##[error]Failed to run: Error: Unexpected HTTP response: 503, Error: Unexpected HTTP response: 503`
- evidence: `##[error]Failed to run: Error: Unexpected HTTP response: 503, Error: Unexpected HTTP response: 503`
- note: runner provisioning/communication failure
- jobs: Validate source code changes
- seen: 2026-08-12 → 2026-08-12
### PRODUCT_RACE (0.90, llm) — 1 occurrence(s)
- signature: `# [TIME] Error: cannot bind tcp port :NUM: address already in use`
- evidence: `Error: cannot bind tcp port :5453: address already in use`
- note: The error indicates that the port is already in use, suggesting a race condition where multiple tests or processes are trying to bind to the same port simultaneously.
- jobs: sys local root fedora-prior
- seen: 2026-08-04 → 2026-08-04
### TEST_BUG (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `config-port`, never re-run to green — likely that PR's regression, not a flake
- signature: `# Error: unmarshalling into &types.PlayKubeReport{Pods:[]types.PlayKubePod(nil), Volumes:[]types.PlayKubeVolume(nil), PlayKubeTeardown:types.PlayKubeTeardown{StopReport:[]*types.PodStopReport{(*types.PodStopReport)(0xa43e90d8680)}, RmReport:[]*types.PodRmReport{(*types.PodRmReport)(0xa43e8e92510)}, VolumeRmReport:[]*types.VolumeRmReport(nil), SecretRmReport:[]*types.SecretRmReport{}}, Secrets:[]types.PlaySecret(nil), ServiceContainerID:"", ValidationWarnings:[]string(nil), ExitCode:(*int32)(nil)}, data "{\"Pods\":null,\"Volumes\":null,\"StopReport\":[{\"Errs\":[\"stopping container HEX: committing transaction to add exit code: disk I/O error: resource temporarily unavailable\",\"stopping container HEX: a container that depends on container HEX could not be stopped: container state improper\"],\"Id\":\"HEX\",\"RawInput\":\"liveness-exec-t459-kgiybdrv-unhealthy\"}],\"RmReport\":[{\"RemovedCtrs\":{\"HEX\":null,\"HEX\":null},\"Err\":null,\"Id\":\"HEX\"}],\"VolumeRmReport\":null,\"SecretRmReport\":[],\"Secrets\":null,\"ServiceContainerID\":\"\",\"ValidationWarnings\":null,\"ExitCode\":null}\n": json: cannot unmarshal string into Go struct field PodStopReport.PlayKubeTeardown.StopReport.Errs of type error`
- evidence: `#| FAIL: exit code is 125; expected 0`
- note: The failure indicates that the test expected an exit code of 0 but received 125 instead, suggesting a bug in the test logic or the code under test. Additionally, the error message about unmarshalling indicates a potential issue with how data is being processed in the test.
- jobs: sys remote rootless fedora-current
- seen: 2026-08-11 → 2026-08-11
### PRODUCT_RACE (1.00, regex) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `# Error: unable to obtain cgroup stats: read /sys/fs/cgroup/machine.slice/libpod-HEX.scope/memory.stat: no such device`
- evidence: `# Error: unable to obtain cgroup stats: read /sys/fs/cgroup/machine.slice/libpod-3520a47b3703d9acad1d634c887ba84d666ec693a48ab18a1a8677789f69149e.scope/memory.stat: no such device`
- note: cgroup removed between existence check and read (stats ENODEV race)
- jobs: sys local root fedora-rawhide
- seen: 2026-08-12 → 2026-08-12
### UNKNOWN (0.00, llm) — 1 occurrence(s)
- signature: `# Error: unable to copy from source docker-archive:/tmp/podman_bats.Udbsfa/archive.tar: writing blob: adding layer with blob "sha256:HEX"/""/"sha256:HEX": unpacking failed (error: exit status 1; output: mkdir /run: no such file or directory)`
- jobs: sys local root fedora-rawhide
- seen: 2026-08-11 → 2026-08-11
### RUNNER_INFRA (0.90, llm) — 1 occurrence(s)
- signature: `# Error: killing container HEX: committing transaction to add exit code: disk I/O error: resource temporarily unavailable`
- evidence: `# Error: killing container 81648c4831f1f88c31d05ad326fac6b0a743a69b0e8c3f7ed35e80825ae4a573: committing transaction to add exit code: disk I/O error: resource temporarily unavailable`
- note: The failure is related to a disk I/O error, indicating a potential issue with the infrastructure where the tests are being run. This suggests a problem with the runner's ability to access necessary resources.
- jobs: sys local rootless debian-sid
- seen: 2026-08-10 → 2026-08-10
### RUNNER_INFRA (0.90, llm) — 1 occurrence(s) · ⚠ confined to branch `fix-xfs-quota-selinux`, never re-run to green — likely that PR's regression, not a flake
- signature: `# Error: copying layers and metadata for container "HEX": writing blob: adding layer with blob "sha256:HEX"/""/"sha256:HEX": lstat /home/ubuntu.guest/.local/share/containers/storage/overlay/tempdirs/temp-dir-NUM/0-addition: no such file or directory`
- evidence: `# Error: copying layers and metadata for container "0a8a8797ec1075461d7ad0b4ce05985a714fd4cf415566cf09be0882a9fc4bfb": writing blob: adding layer with blob "sha256:26d4ed1d17075cce1b19308d3d016b2d189eee732597e17d4774a9e0b5766855"/""/"sha256:26d4ed1d17075cce1b19308d3d016b2d189eee732597e17d4774a9e0b5766855": lstat /home/ubuntu.guest/.local/share/containers/storage/overlay/tempdirs/temp-dir-1024368511/0-addition: no such file or directory`
- note: The error indicates a failure related to the file system where the container layers are being written, suggesting an issue with the runner's infrastructure. The specific 'no such file or directory' message points to a problem in the environment where the tests are executed.
- jobs: sys local rootless fedora-rawhide
- seen: 2026-08-11 → 2026-08-11
### TEST_BUG (0.90, llm) — 1 occurrence(s) · 1 re-run-confirmed
- signature: `# Error: committing container for step {Env:[PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin] Command:run Args:[mkdir /mountroot && echo data file inside the IMAGE - JrNUTk4NW3mEXYc > /mountroot/data] Flags:[] Attrs:map[] Message:RUN mkdir /mountroot && echo data file inside the IMAGE - JrNUTk4NW3mEXYc > /mountroot/data Heredocs:[] Original:RUN mkdir /mountroot && echo data file inside the IMAGE - JrNUTk4NW3mEXYc > /mountroot/data}: copying layers and metadata for container "HEX": writing blob: adding layer with blob "sha256:HEX"/""/"sha256:HEX": unpacking failed (error: exit status 1; output: mkdir /mountroot: no such file or directory)`
- evidence: `# Error: committing container for step {Env:[PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin] Command:run Args:[mkdir /mountroot && echo data file inside the IMAGE - JrNUTk4NW3mEXYc > /mountroot/data] Flags:[] Attrs:map[] Message:RUN mkdir /mountroot && echo data file inside the IMAGE - JrNUTk4NW3mEXYc > /mountroot/data Heredocs:[] Original:RUN mkdir /mountroot && echo data file inside the IMAGE - JrNUTk4NW3mEXYc > /mountroot/data}: copying layers and metadata for container "21d4d48f6471c65838dd3008d513a7d72c9fab91941a601e1e478f8a9cdaf21e": writing blob: adding layer with blob "sha256:ad683f72dfe3b991d278c7beed528d6cd92d7ba768330709db42161b0f142664"/""/"sha256:11da3b82027e1ffdbd863db8dfcb8c70376847ab320fda2eea0e5504815653c0": unpacking failed (error: exit status 1; output: mkdir /mountroot: no such file or directory)`
- note: The error indicates that the test is failing due to a command trying to create a directory that does not exist, which suggests a bug in the test setup or the command being executed. This is not a network or infrastructure issue, but rather a problem with the test itself.
- jobs: sys local rootless debian-sid
- seen: 2026-08-09 → 2026-08-09
### NETWORK_INFRA (1.00, llm) — 1 occurrence(s)
- signature: `# Error: Get "https://raw.githubusercontent.com/containers/podman/main/test/build/from-scratch/Dockerfile": net/http: TLS handshake timeout`
- evidence: `# Error: Get "https://raw.githubusercontent.com/containers/podman/main/test/build/from-scratch/Dockerfile": net/http: TLS handshake timeout`
- note: The failure is due to a TLS handshake timeout when trying to access a remote resource, indicating a network-related issue.
- jobs: sys local rootless fedora-rawhide
- seen: 2026-08-07 → 2026-08-07
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
