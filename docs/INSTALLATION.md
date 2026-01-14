# Installation Guide

Complete installation instructions for Arete across different platforms.

## Prerequisites

Before you begin, ensure you have the following installed:

| Requirement | Version | Check Command | Installation Guide |
|-------------|---------|---------------|-------------------|
| Docker | 20.10+ | `docker --version` | [Install Docker](#docker-installation) |
| Docker Compose | 2.0+ | `docker-compose --version` | Included with Docker Desktop |
| Git | 2.30+ | `git --version` | [git-scm.com](https://git-scm.com/downloads) |
| Python | 3.10+ | `python3 --version` | [python.org](https://www.python.org/downloads/) |

## Docker Installation

### Windows - Docker Desktop

**Requirements:**
- Windows 10/11 64-bit
- WSL 2 enabled (recommended) or Hyper-V

**Steps:**

1. **Download Docker Desktop for Windows**
   - Go to [Docker Desktop download page](https://www.docker.com/products/docker-desktop)
   - Click "Download for Windows"
   - Or visit the [Windows install docs](https://docs.docker.com/desktop/setup/install/windows-install/)

2. **Run the installer**
   - Double-click `Docker Desktop Installer.exe` from your Downloads folder
   - Leave WSL 2 selected when asked about backend (recommended)

3. **Follow the wizard**
   - Accept the license terms
   - Keep default settings
   - Wait for installation to complete, then click Close

4. **(If needed) Add your user to docker-users group**
   - Only necessary if your admin account differs from your user account

5. **Restart Windows**
   - Reboot so configuration and services are fully applied

6. **Verify Docker**
   ```bash
   docker --version
   docker run hello-world
   ```
   You should see Docker version info and a "Hello from Docker!" message.

📚 **Official docs:** [Windows install](https://docs.docker.com/desktop/setup/install/windows-install/)

---

### Linux (Ubuntu) - Docker Engine

**Requirements:**
- Ubuntu 22.04/24.04 (or other supported release)
- `sudo` access and internet connection

**Steps:**

1. **Uninstall old Docker** (optional but recommended)
   ```bash
   sudo apt remove docker docker-engine docker.io containerd runc
   ```

2. **Update package index**
   ```bash
   sudo apt update
   ```

3. **Install prerequisites**
   ```bash
   sudo apt install ca-certificates curl gnupg
   ```

4. **Add Docker's official GPG key**
   ```bash
   sudo install -m 0755 -d /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
     | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   sudo chmod a+r /etc/apt/keyrings/docker.gpg
   ```

5. **Set up the Docker apt repository**
   ```bash
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
     https://download.docker.com/linux/ubuntu \
     $(. /etc/os-release && echo ${UBUNTU_CODENAME:-$VERSION_CODENAME}) stable" \
   | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

6. **Update package index again**
   ```bash
   sudo apt update
   ```

7. **Install Docker Engine + CLI + plugins**
   ```bash
   sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```
   This installs Docker Engine, CLI, containerd, Buildx, and Docker Compose plugin.

8. **Enable Docker at boot** (usually automatic)
   ```bash
   sudo systemctl enable docker
   sudo systemctl status docker
   ```

9. **Verify Docker**
   ```bash
   sudo docker run hello-world
   ```

10. **(Optional) Run Docker without sudo**
    ```bash
    sudo groupadd docker        # may say group exists, that's fine
    sudo usermod -aG docker $USER
    newgrp docker
    docker run hello-world
    ```

📚 **Official docs:** [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
📖 **Tutorial:** [DigitalOcean guide for Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)

---

### macOS - Docker Desktop

**Requirements:**
- macOS on Intel or Apple Silicon (M1/M2/M3) with a supported macOS version
- At least 4 GB RAM

**Steps:**

1. **Download Docker Desktop for Mac**
   - Go to [Docker Desktop download page](https://www.docker.com/products/docker-desktop)
   - Choose "Mac with Intel" or "Mac with Apple silicon"

2. **Open the installer**
   - Double-click `Docker.dmg` in your Downloads folder

3. **Install Docker Desktop**
   - Drag the Docker icon to the Applications folder
   - Docker Desktop will be installed at `/Applications/Docker.app`

4. **Launch Docker Desktop**
   - Open **Applications → Docker** or use Spotlight (⌘+Space → type "Docker" → Enter)
   - The whale icon appears in the menu bar; wait until it stops animating (Docker is ready)

5. **Grant permissions if asked**
   - Enter your macOS password or use Touch ID when prompted

6. **Verify Docker**
   ```bash
   docker --version
   docker run hello-world
   ```
   You should see Docker version info and the "Hello from Docker!" message.

📚 **Official docs:** [Mac install](https://docs.docker.com/desktop/setup/install/mac-install/)
📖 **Guide:** [Install Docker Desktop on Mac](https://dev.to/pwd9000/install-docker-desktop-on-mac-1omo)

---

## Verifying Installation

After installing Docker, verify your setup:

```bash
# Check versions
docker --version
docker-compose --version
git --version
python3 --version

# Test Docker
docker run hello-world

# Check Docker Compose
docker-compose --version
```

## Next Steps

After installation is complete:

1. **Configure API Keys**: See [API_KEYS.md](API_KEYS.md) for Supabase and Anthropic setup
2. **Run Setup**: Execute the setup script from the main README
3. **Start Application**: Use `docker-compose up --build`

## Troubleshooting

### Docker not starting on Windows
- Ensure WSL 2 is installed and updated
- Check virtualization is enabled in BIOS
- Restart Docker Desktop service

### Permission denied on Linux
- Add your user to docker group: `sudo usermod -aG docker $USER`
- Log out and back in for changes to take effect

### Docker Desktop stuck on starting (macOS)
- Quit Docker Desktop completely
- Clear Docker Desktop data: `rm -rf ~/Library/Group\ Containers/group.com.docker`
- Restart Docker Desktop

For more issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
