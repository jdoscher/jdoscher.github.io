---
title: "Tech Stack: Down the Rabbit Hole with GPU Passthrough for Intel Integrated Graphics on Linux"
date: 2024-07-13
slug: gpu-passthrough-for-intel
tags: []
description: 
canonical_url: 
layout: post
---
<p>I had a unique task this last week to test integrated graphics passthrough from a Proxmox host to a virtual machine guest, then to a docker container on the virtual machine.  I don't have a ton of commentary to add, but I do want to share the collection of configurations needed to do so, especially since the Intel N100 does this kind of hardware work on single digit watt energy loads.  I'm collecting everything here for folks to find later.</p><h3 id="proxmox-host-configuration">Proxmox Host Configuration</h3><p>In order to pass the GPU (in this case the embedded GPU on the Intel N100), you will need to bypass video output on your Proxmox host.  This will probably limit the kinds of workloads you will want to put on this host, since you won't have access to the local console with this approach.  With larger multi-GPU units this may behave differently, but for this one assume everything will be remote besides the BIOS.  You can install Proxmox VE normally, and I recommend you do so before "losing" the local console.</p><p>First, make a backup of your existing grub config with </p><p><code>cp /etc/default/grub /etc/default/grub.original</code></p>
<p>Then open the default grub file on the Proxmox host with:</p><p><code>nano /etc/default/grub </code></p>
<p>Find the line that says this:</p><p><code>GRUB_CMDLINE_LINUX_DEFAULT="quiet" </code></p>
<p>And change it to this- it still includes the quiet option, but adds the hardware info- this keeps the local Proxmox host from loading the hardware (like the video transcoder) on the host Linux install.</p><p><code>GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt pcie_acs_override=downstream,multifunction initcall_blacklist=sysfb_init video=simplefb:off video=vesafb:off video=efifb:off video=vesa:off disable_vga=1 vfio_iommu_type1.allow_unsafe_interrupts=1 kvm.ignore_msrs=1 modprobe.blacklist=radeon,nouveau,nvidia,nvidiafb,nvidia-gpu,snd_hda_intel,snd_hda_codec_hdmi,i915" </code></p>
<p>All of that will be on one line- make sure the text formatting wraparound doesn't get lost in the copy/paste. Save the file and return to the command console/terminal.</p><p>Run the update command to have grub process the config changes with:</p><p><code>update-grub</code></p>
<p>Now edit the modules file with:</p><p><code>nano /etc/modules</code></p>
<p>Add the following lines:</p><pre><code class="language-vfio_pci">vfio
vfio_virqfd
vfio_iommu_type1
</code></pre>
<p>And run this to load the new modules:</p><p><code>update-initramfs -u -k all </code></p>
<p>After this, reboot and return to the Proxmox terminal, through the web interface or the ssh prompt. Run this command after the reboot to verify the hardware has taken properly:</p><p><code>dmesg | grep -e DMAR -e IOMMU </code></p>
<p>You should see several lines including these: </p><pre><code>DMAR: IOMMU enabled
DMAR: Host address width 39
</code></pre>
<p>This is your indication that the Proxmox host has been configured and ready for the virtual machine guest setup.</p><h3 id="proxmox-guest-virtual-machine-configuration">Proxmox Guest Virtual Machine Configuration</h3><p>Next we'll need to configure a guest to use the hardware available as passed through from the host.  Simply create the VM as you would normally through the wizard, but do not start the VM.  After it has been provisioned, select it and go to the 'Hardware' section in the VM's configuration and select 'Add'.  Select 'PCI Device'.  It should be labeled something like:</p><pre><code>0000:00:02,pcie=1
</code></pre>
<p>Since this can only be passed through to a single VM, you cannot share this GPU between VMs.  It also appears that Proxmox will not let you assign it to more than one VM at a time either, so doing any failover between nodes would likely need some additional scripting or automation.</p><p>From here you are ready to install your OS on the guest virtual machine.  For this example we'll use Ubuntu, but in theory any x86 compatible OS should be fine, so long as it supports the integrated GPU.  Since our plan is to leverage this for photo processing, we are using Ubuntu for Photoprism.</p><h3 id="guest-operation-system-configuration">Guest Operation System Configuration</h3><p>Install Ubuntu and configure a user that the Docker container will run under.  I recommend giving the new user sudo access to make this easier, then revoking when setup is done.  You can also just have a second terminal with your sudo user running for those commands too.</p><p>First check and see if the renderD128 device is present with this command:</p><p><code>ls -l /dev/dri/</code></p>
<p>It should show you something like this:</p><p><code>crw-rw---- 1 root render 226, 128 Jul  2 21:41 renderD128</code></p>
<p>This is good and means the integrated GPU has been passed from the host to the guest VM.  Now run this command as your sudo user to add your docker user (in this case my photoprism user photo_prism_user) to the render group, giving that user access to device itself.</p><p><code>sudo usermod -aG render photo_prism_user</code></p>
<p>Since group membership is applied at login, you will need to log out of photo_prism_user and log back in to have it applied.  Check the docker post-installation instructions and follow that for group membership too, since it is outside the scope of this article to setup docker- that group membership will require a log out and log in too.</p><p>Now you're ready to configure the docker container.  Remember to do all your docker host config steps before continuing.</p><h3 id="docker-container-configuration">Docker Container Configuration</h3><p>Finally in your docker compose file, you will need a couple settings.  First, for our Photoprism user we need to call out the UID and GID of that user.  You can get it with these commands:</p><pre><code>id -u photo_prism_user
id -g photo_prism_user
</code></pre>
<p>Now that we have that info, we can assign them properly in the docker-compose yaml for Photoprism.  Keep in mind the PUID and PGID will assign the user to this docker container, so file permissions for things like photos and other mounted folders need to allow the photo_prism_user access to those as well.  Watch your indents on this code block!</p><pre><code class="language-devices:">      - /dev/dri/renderD128:/dev/dri/renderD128
    environment:
      - PUID=1003
      - PGID=1003</code></pre>
<p>That's it!  Things may get complicated with more complex group permissions for the docker container, but I am hopeful this can be used outside of just the render devices in the future, especially as hardware for more complex AI and LLM jobs come into play.  This could also potentially work for NVIDIA GPU's as well, but for my small hosting setup the Intel N100 is plenty. </p><p></p><p></p>
