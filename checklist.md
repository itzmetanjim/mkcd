## Coverage Checklist (grouped by category)

Use this as the master checklist for what to bundle or map. Check off as you implement.

### Detected / checked (from available EXE binaries)

- [x] base64
- [x] bunzip2
- [x] bzip2
- [x] cat
- [x] chmod
- [x] chown
- [x] column
- [x] comm
- [x] cp
- [x] cut
- [x] date
- [x] df
- [x] du
- [x] expand
- [x] fmt
- [x] fold
- [x] awk (gawk/mawk/nawk—choose one) — gawk
- [x] grep
- [x] gzip
- [x] head
- [x] hostname
- [x] id
- [x] install
- [x] join
- [x] ls
- [x] ln
- [x] md5sum
- [x] mkdir
- [x] mv
- [x] nl
- [x] od
- [x] paste
- [x] pwd
- [x] readlink
- [x] realpath
- [x] rm
- [x] rmdir
- [x] sed
- [x] sha1sum
- [x] sha256sum
- [x] sort
- [x] split
- [x] stat
- [x] sync
- [x] tee
- [x] tar
- [x] tail
- [x] touch
- [x] tr
- [x] truncate
- [x] uniq
- [x] unexpand
- [x] unxz
- [x] uname
- [x] wc
- [x] which
- [x] whoami
- [x] xargs
- [x] xz
- [x] csplit

Remaining (not found among provided EXE files)

- dir, vdir
- tac
- hexdump
- strings
- egrep (compat)
- fgrep (compat)
- rev
- ptx
- locate
- updatedb
- whereis
- cpio
- pax
- zip
- unzip
- gunzip
- zcat
- bzcat
- xzcat
- zstd
- unzstd
- sha224sum
- sha384sum
- sha512sum
- shasum
- cksum
- sum
- env
- printenv
- yes
- true
- false
- test
- expr
- seq
- timeout
- nice
- nohup
- stty
- tput
- groups
- logname
- who
- users
- nproc
- uptime
- ps
- kill
- pkill
- pgrep
- top
- watch
- diff
- sdiff
- diff3
- cmp
- patch
- file
- curl
- wget
- ping
- traceroute
- nc (netcat)
- telnet
- dig
- host
- nslookup
- ssh
- scp
- sftp
- tree
- mktemp
- uuencode/uudecode
- factor
- numfmt
- pathchk
- base32
- shuf
- tsort
- cd
- pushd/popd
- alias/unalias
- time
- any other duplicates noted in the main checklist (resolve after insertion)

Core file/directory and metadata (Coreutils-ish)

Color-capable (accept "--color=auto"): ls, grep

- [ ] ls
- [ ] dir, vdir (optional)
- [ ] cp
- [ ] mv
- [ ] rm
- [ ] rmdir
- [ ] mkdir
- [ ] install
- [ ] ln
- [ ] readlink
- [ ] realpath
- [ ] stat
- [ ] touch
- [ ] chmod
- [ ] chown
- [ ] chgrp
- [ ] umask
- [ ] pwd
- [ ] du
- [ ] df
- [ ] sync
- [ ] truncate

Text processing and filtering

- [ ] cat
- [ ] tac
- [ ] head
- [ ] tail
- [ ] nl
- [ ] wc
- [ ] cut
- [ ] paste
- [ ] join
- [ ] sort
- [ ] uniq
- [ ] tr
- [ ] od
- [ ] hexdump (optional)
- [ ] strings (optional)
- [ ] fold
- [ ] fmt
- [ ] column
- [ ] expand
- [ ] unexpand
- [ ] sed
- [ ] awk (gawk/mawk/nawk—choose one)
- [ ] grep
- [ ] egrep (compat)
- [ ] fgrep (compat)
- [ ] xargs
- [ ] tee
- [ ] rev (optional)
- [ ] split
- [ ] csplit
- [ ] comm
- [ ] ptx (optional)

Search / filesystem traversal

- [ ] find
- [ ] locate (optional; requires database)
- [ ] updatedb (optional; for locate DB)
- [ ] which
- [ ] whereis (optional)

Archiving and compression

- [ ] tar
- [ ] cpio (optional)
- [ ] pax (optional)
- [ ] zip
- [ ] unzip
- [ ] gzip
- [ ] gunzip (gzip -d)
- [ ] zcat (gzip -cd)
- [ ] bzip2
- [ ] bunzip2 (bzip2 -d)
- [ ] bzcat (bzip2 -cd)
- [ ] xz
- [ ] unxz (xz -d)
- [ ] xzcat (xz -cd)
- [ ] zstd
- [ ] unzstd (zstd -d)

Checksums, hashes, encoding

- [ ] md5sum
- [ ] sha1sum
- [ ] sha224sum
- [ ] sha256sum
- [ ] sha384sum
- [ ] sha512sum
- [ ] shasum (optional, perl-based)
- [ ] cksum
- [ ] sum
- [ ] base64

Environment and session

- [ ] env
- [ ] printenv
- [ ] yes
- [ ] true
- [ ] false
- [ ] test
- [ ] expr
- [ ] seq
- [ ] tee
- [ ] timeout
- [ ] nice
- [ ] nohup
- [ ] stty (optional)
- [ ] tput (optional)

System info and identity

- [ ] uname
- [ ] hostname
- [ ] whoami
- [ ] id
- [ ] groups
- [ ] logname
- [ ] who
- [ ] users
- [ ] date
- [ ] nproc
- [ ] uptime (optional; non-coreutils on Linux)

Process and signals

- [ ] ps
- [ ] kill
- [ ] pkill
- [ ] pgrep
- [ ] top (optional)
- [ ] watch (optional)

Diff/patch and build helpers

- [ ] diff
- [ ] sdiff
- [ ] diff3
- [ ] cmp
- [ ] patch
- [ ] file

Networking/transfer

- [ ] curl
- [ ] wget
- [ ] ping
- [ ] traceroute (optional; Windows needs admin/ICMP permission or an alternative)
- [ ] nc (netcat)
- [ ] telnet (optional)
- [ ] dig (optional; from bind9/dnsutils)
- [ ] host (optional)
- [ ] nslookup (optional)
- [ ] ssh (optional; from OpenSSH)
- [ ] scp (optional)
- [ ] sftp (optional)

Miscellaneous convenience

- [ ] tree (optional)
- [ ] realpath (duplicate noted above; ensure single implementation)
- [ ] mktemp
- [ ] uuencode/uudecode (optional)
- [ ] factor (optional)
- [ ] numfmt (optional)
- [ ] pathchk (optional)
- [ ] base32 (optional)
- [ ] shuf (optional)
- [ ] tsort (optional)
- [ ] timeout (duplicate noted above)
- [ ] watch (duplicate noted above)

## Builtins to wrap or emulate (opt-in)

Some commands are typically builtins but are useful to expose as pipe-aware helpers.

- [ ] cd (shell builtin; wrap to accept pipeline)
- [ ] pushd/popd (optional pipe-aware variants)
- [ ] alias/unalias (optional)
- [ ] time (shell keyword; provide external wrapper if desired)
