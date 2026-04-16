# EndeavourOS Update & Maintenance Guide

> For my EndeavourOS (Arch) system: full system upgrades, AUR management, common issues, and housekeeping.

---

## 1. Core Principles (Arch / EndeavourOS)

1. **No partial upgrades.**  
   Always upgrade the whole system together (`-Syu`), never just a few random packages from refreshed databases. Partial upgrades are explicitly unsupported in Arch and can break things.

2. **Read the news before big upgrades.**
   - Check **Arch Linux news** (manual interventions, breaking changes).
   - Glance at **EndeavourOS forum announcements** (e.g., eos-update issues, manual intervention notes).

3. **Use a single AUR helper (yay or paru) consistently.**
   - EndeavourOS community heavily leans on `yay`/`paru` as a “one-stop” updater for both repo and AUR.

4. **Update regularly.**
   - Ideal: every **2–3 days**.
   - Acceptable: **at least weekly**.  
     Leaving it for months increases the chance of big, painful transitions.

---

## 2. Full System Upgrade Workflow

You can either:

- **Option A (simple, recommended): use yay only**
- **Option B: pacman for repos, yay for AUR**

Pick one style and stick with it.

### 2.1 Option A – One Command (yay-only)

This is the most convenient on EndeavourOS:

```bash
yay
# equivalent to yay -Syu (full repo + AUR upgrade)
# ehhh just do
yay -Syu
```

`yay` will:

- Sync repo databases
- Upgrade all **official repo** packages
- Upgrade all **AUR** packages

Use this as your default “update everything” command.

---

### 2.2 Option B – pacman first, then AUR

If you prefer to separate repo and AUR updates:

```bash
# 1. Official repos
sudo pacman -Syu

# 2. AUR only
yay -Sua
```

- `-Syu` = sync + refresh databases + upgrade system
- `-Sua` = upgrade only AUR packages

---

### 2.3 Pre-update checklist (every run)

1. **Check Arch news (quick scan):**
   - https://archlinux.org/news/  
     Look for anything mentioning `manual intervention`, kernel, `glibc`, `systemd`, `linux-firmware`, etc.

2. **Check EndeavourOS announcements** (optional but nice):
   - Especially if something just broke, scan the EndeavourOS forum “Announcements and news”.

3. **Run your updater** (`yay` or `sudo pacman -Syu && yay -Sua`).

4. **Actually read pacman/yay output** – don’t just mash Enter.

---

## 3. AUR Package Management & Cleanbuilds

### 3.1 Installing / updating AUR packages

- **Search & install:**

  ```bash
  yay -Ss package-name
  yay -S package-name
  ```

- **Update all AUR packages (only):**

  ```bash
  yay -Sua
  ```

- **Include VCS (`*-git`, `*-hg`, etc.) packages:**

  ```bash
  yay -Syu --devel
  ```

  Do this **weekly-ish**, not necessarily every day.

### 3.2 “Packages to cleanBuild?” – What to do

When `yay` asks:

> `Packages to cleanBuild? [N]`

It’s asking whether to **reclone and rebuild those AUR packages from scratch**, discarding old build artifacts. Basically `rm -rf` old sources + fresh build.

**Guideline:**

- After _normal_ small updates → **leave default (None / N)**.
- After **big transitions** (new `glibc`, major `rust/go/clang`, big Electron changes, etc.) OR if a package misbehaves:
  - Answer with package numbers (or `All`) to **cleanbuild** those.

You can also trigger it manually:

```bash
# Cleanbuild a single AUR package
yay -S google-chrome --cleanbuild

# Rebuild + cleanbuild if it’s really borked
yay -S google-chrome --rebuildtree --cleanbuild
```

### 3.3 Good AUR hygiene

- **Read the PKGBUILD and comments** when installing something new.
- Prefer **well-maintained, popular** AUR packages when possible.
- If a build fails:
  1. Read the **AUR comments** for that package.
  2. Make sure your system is fully updated.
  3. Try `--cleanbuild` or `--rebuildtree`.
  4. If it’s a real bug, wait for the maintainer or patch manually with `yay -G` + `makepkg`.

---

## 4. Common Issues & How to Fix Them

### 4.1 PGP / signature errors

Typical messages:

- `invalid or corrupted package (PGP signature)`
- `key XYZ could not be looked up remotely`

**Fix (repo packages):**

```bash
sudo pacman -Sy archlinux-keyring
sudo pacman -Syu
```

If needed:

```bash
sudo pacman-key --refresh-keys
```

**For AUR PGP errors**:  
Check the AUR comments – often you must manually import the maintainer’s key with `gpg --recv-key <KEYID>`.

---

### 4.2 File conflicts (file already exists in filesystem)

Message:

> `conflicting file /path/to/file exists in filesystem`

Cause: file leftover from a manual install, old package, or moved path.

Typical fix:

1. Inspect the file:
   ```bash
   ls -l /path/to/file
   ```
2. If you’re sure it belongs to the package you’re installing/upgrading:
   - Remove it **or**
   - Force overwrite:
     ```bash
     sudo pacman -S package-name --overwrite /path/to/file
     ```

Double-check before forcing overwrites.

---

### 4.3 .pacnew / .pacsave config files

During updates, pacman may leave config files like:

- `/etc/pacman.conf.pacnew`
- `/etc/someconfig.conf.pacnew`

Best practice:

- **Merge changes** instead of blindly copying or ignoring.

Tools:

```bash
sudo pacdiff   # from pacman-contrib, uses a $DIFFPROG like vimdiff, meld, etc.
```

On EndeavourOS you may also have helper scripts (e.g., eos-\* tools) that wrap pacdiff.

---

### 4.4 “Manual intervention required”

If pacman/yay says anything like:

> `:: (1/1) Install something requires manual intervention`  
> `See https://archlinux.org/news/...`

or EndeavourOS announces an issue with `eos-update` or similar:

**Do this:**

1. **Stop the upgrade. Do not continue blindly.**
2. Open the URL from the message.
3. Follow the manual steps exactly (often a couple of commands or edits).
4. Re-run your `yay`/`pacman` update afterwards.

---

### 4.5 Broken AUR app after update

Symptoms: it builds, but crashes or won’t start.

Fix:

1. Full update again (repo + AUR), just in case.
2. Clean rebuild the app:

   ```bash
   yay -S app-name --rebuildtree --cleanbuild
   ```

3. If it still fails, check the AUR comments / bug tracker – could be an upstream issue.

---

## 5. Housekeeping & Maintenance Cadence

### 5.1 Every 2–3 days (or at least weekly)

- **Update system + AUR:**

  ```bash
  yay        # or: sudo pacman -Syu && yay -Sua
  ```

- Quickly review:
  - Any **news / manual intervention**?
  - Any `.pacnew` files that need merging?

---

### 5.2 Monthly (or every 1–2 months)

#### 5.2.1 Clean journal logs

Keep ~4 weeks of logs:

```bash
sudo journalctl --vacuum-time=4weeks
```

#### 5.2.2 Clean pacman package cache

`paccache` (from `pacman-contrib`) keeps 3 versions by default:

```bash
sudo paccache -r
```

If disk is _really_ tight, you can keep only 1 version:

```bash
sudo paccache -rk1
```

#### 5.2.3 Remove orphan packages

Orphans = installed as dependencies but not needed anymore.

**Check first**:

```bash
pacman -Qdt
```

If you’re comfortable removing them:

```bash
sudo pacman -Rns $(pacman -Qdtq)
```

---

### 5.3 Occasionally / as needed

- **Clean yay cache & build directories**:

  ```bash
  yay -Sc   # safely clear unused package files
  # yay -Scc  # nukes *all* cached packages (be sure you want this)
  ```

- **Mirror updates** (when downloads feel slow or you move regions):  
  Use EndeavourOS tools or `reflector` to refresh mirrors, then do a full `yay -Syyu` once after changing mirrors.

---

## 6. Quick Reference Cheat Sheet

**Daily / Every Few Days**

```bash
# 1. (Optional) glance at news:
#    https://archlinux.org/news/ + EndeavourOS forum Announcements

# 2. Update system & AUR
yay
# or:
sudo pacman -Syu
yay -Sua
```

**When yay asks “Packages to cleanBuild?”:**

- Normal day: **None** (default).
- After big toolchain / library changes, or if an app is weird:  
  select the relevant packages or `All`.

**If signatures/keys fail:**

```bash
sudo pacman -Sy archlinux-keyring
sudo pacman -Syu
# maybe:
sudo pacman-key --refresh-keys
```

**Monthly-ish**

```bash
# Clean logs
sudo journalctl --vacuum-time=4weeks

# Clean pacman cache (keep 3 versions)
sudo paccache -r

# Remove orphans (after checking!)
pacman -Qdt
sudo pacman -Rns $(pacman -Qdtq)
```

**AUR-specific**

```bash
# AUR-only upgrades
yay -Sua

# Include VCS packages
yay -Syu --devel

# Fix a broken AUR app
yay -S app-name --rebuildtree --cleanbuild
```
