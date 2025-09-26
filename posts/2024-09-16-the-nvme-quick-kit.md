---
title: "The NVME Quick Kit"
date: 2024-09-16
slug: the-nvme-quick-kit
tags: []
description: 
canonical_url: 
layout: post
---
<p>Most of my deck builds are concepts, intended to be as open-ended as possible.  Today I'm sharing one with a very specific purpose- to sync critical data as securely as possible.</p><p>"Securely" will mean a wide spectrum of different things to different people, but for me I want a host with a copy of data that can't easily be accessed from other systems.  This is almost a one-way copy box.  What is different here is that I'm not just showing the design this time, I am going to give some specific examples of how I'm doing it, and how you can too.</p><p>While the designs are for paid subscribers, the code here is all human-tested and works fine with my specific use case.  I encourage you to do your own reading to make sure you are comfortable with these commands, as you are responsible for your own data.</p><p>I'll also provide some insights on the hardware at the end of the article too- since running two <a href="https://en.wikipedia.org/wiki/NVM_Express" rel="noreferrer">NVME </a>drives on a Raspberry Pi 5 pulls more than the dusty old Raspberry Pi 4.</p><figure class="kg-card kg-image-card"><img src="/images/content/images/2024/08/JAY00382.jpg" class="kg-image" alt="" loading="lazy" width="2000" height="1333" srcset="/images/content/images/size/w600/2024/08/JAY00382.jpg 600w, /images/content/images/size/w1000/2024/08/JAY00382.jpg 1000w, /images/content/images/size/w1600/2024/08/JAY00382.jpg 1600w, /images/content/images/2024/08/JAY00382.jpg 2000w" sizes="(min-width: 720px) 720px"></figure><p>For this build there's an opening at the bottom- the design files include a snap-in cover for it in case you want it, but the hole helps a little with ventilation and it provides a good handle for popping the unit out of the Pelican case.</p><figure class="kg-card kg-image-card"><img src="/images/content/images/2024/08/JAY00383.jpg" class="kg-image" alt="" loading="lazy" width="2000" height="1333" srcset="/images/content/images/size/w600/2024/08/JAY00383.jpg 600w, /images/content/images/size/w1000/2024/08/JAY00383.jpg 1000w, /images/content/images/size/w1600/2024/08/JAY00383.jpg 1600w, /images/content/images/2024/08/JAY00383.jpg 2000w" sizes="(min-width: 720px) 720px"></figure><p>As usual, no modifications are required to the Pelican 1150.  The 3D parts are a single face frame, along with 4 small risers and a rear frame with slots for a zip tie or two, just in case.  Here's the parts list:</p><ul>
<li>Pelican 1150 Case: <a href="https://amzn.to/3Twgr8W">Amazon</a></li>
<li>Raspberry Pi 5 8GB (2GB would work just a fine for copy jobs): <a href="https://amzn.to/4e9Jh7u">Amazon</a>, <a href="https://www.adafruit.com/product/5813">Adafruit</a></li>
<li>Official Raspberry Pi Heatsink &amp; Fan: <a href="https://amzn.to/47uiBM2">Amazon</a>, <a href="https://www.adafruit.com/product/5815">Adafruit</a></li>
<li>Official Raspberry Pi 7" Display: <a href="https://amzn.to/4epijYS">Amazon</a></li>
<li>Official Raspberry Pi 5 DSI cable: <a href="https://amzn.to/3ZrtFHN">Amazon</a>, <a href="https://www.sparkfun.com/products/23683">Sparkfun</a></li>
<li>Dual NVME Hat for the Raspberry Pi 5: <a href="https://amzn.to/3XuynSF">Amazon</a></li>
<li>M5x10mm (qty 4) Hex Screws: <a href="https://amzn.to/3XKaMyu">Amazon</a> (50) or <a href="https://www.mcmaster.com/91290A224/">McMaster Carr</a> (100)</li>
<li>M3x10mm (qty 10) Hex Screws: <a href="https://amzn.to/3Tw9PaC">Amazon</a> (100) or <a href="https://www.mcmaster.com/91290A115/">McMaster Carr</a> (100)</li>
<li>Panel Mount USB adapters (2 pack): <a href="https://amzn.to/3B5Rn2c">Amazon</a></li>
<li>Panel Mount Ethernet Jack: <a href="https://amzn.to/4gr4vin">Amazon</a></li>
<li>Two Solidigm P41 Plus 1TB NVME Drives (really any couple would work, since you're not going to get full speed out of the NVME ports): <a href="https://amzn.to/47oGV1X">Amazon</a></li>
<li>MicroSD card for the initial boot config this is temporary: <a href="https://amzn.to/3zjYIut">Amazon</a></li>
<li>NVME to USB adapter for imaging the NVME drive: <a href="https://amzn.to/3B7vdg4">Amazon</a></li>
<li>STL Files require at least 1 month membership ($5) and can be cancelled anytime.  Files are in this <a href="www.doscher.com/paid-subscribers-only-nvme-quick-kit-stl-files/">post</a>.</li>
<li>CAD Files are available for a higher fee and are available <a href="www.doscher.com/paid-subscribers-only-nvme-quick-kit-cad-stl-files/">here</a>.</li>
</ul>
<figure class="kg-card kg-image-card"><img src="/images/content/images/2024/08/JAY00385.jpg" class="kg-image" alt="" loading="lazy" width="2000" height="1333" srcset="/images/content/images/size/w600/2024/08/JAY00385.jpg 600w, /images/content/images/size/w1000/2024/08/JAY00385.jpg 1000w, /images/content/images/size/w1600/2024/08/JAY00385.jpg 1600w, /images/content/images/2024/08/JAY00385.jpg 2000w" sizes="(min-width: 720px) 720px"></figure><p>The frame on the back does something fairly important, it keeps you from resting the entire internal chassis on those NVME drives, which are quite fragile.  </p><figure class="kg-card kg-image-card"><img src="/images/content/images/2024/08/JAY00386.jpg" class="kg-image" alt="" loading="lazy" width="2000" height="1333" srcset="/images/content/images/size/w600/2024/08/JAY00386.jpg 600w, /images/content/images/size/w1000/2024/08/JAY00386.jpg 1000w, /images/content/images/size/w1600/2024/08/JAY00386.jpg 1600w, /images/content/images/2024/08/JAY00386.jpg 2000w" sizes="(min-width: 720px) 720px"></figure><p>The prints are Carbon Fiber PETG from Bambu Labs, which seems to hold up to a few cycles of assembly and disassembly, but if you're going to be constantly removing screws from the rear frame, you'll want to redesign with metal inserts.</p><figure class="kg-card kg-image-card"><img src="/images/content/images/2024/08/JAY00387.jpg" class="kg-image" alt="" loading="lazy" width="2000" height="1333" srcset="/images/content/images/size/w600/2024/08/JAY00387.jpg 600w, /images/content/images/size/w1000/2024/08/JAY00387.jpg 1000w, /images/content/images/size/w1600/2024/08/JAY00387.jpg 1600w, /images/content/images/2024/08/JAY00387.jpg 2000w" sizes="(min-width: 720px) 720px"></figure><p>Nestled in there is the stock fan, which seemed to run just fine- but remember these copy jobs will use all the CPU and disk IO you can give them.  If you're a subscriber and you've downloaded the files, thank you!  The assembly is pretty straightforward, and you really just need the Hoto screwdriver, which has the bits you need:</p><ul>
<li>Hoto Electric Screwdriver for the M5 screws (you can do these by hand, but I always use the Hoto for these kinds of screws) - <a href="https://amzn.to/4ejNmFu">Amazon</a></li>
</ul>
<h3 id="but-what-do-you-use-it-for">"But What Do You Use It For?"</h3><p>Well, for this one I use it for keeping backup copies of important configuration files and database exports.  If you're not familiar with the <a href="https://www.backblaze.com/blog/the-3-2-1-backup-strategy/" rel="noreferrer">3-2-1 rule</a>, it's worth taking a quick read.  This build is as much of a defense against others as it is against my tinkering.  I want multiple copies over time of the same data.  Here's how to do it.</p><p>After you've finished following<a href="https://www.jeffgeerling.com/blog/2023/nvme-ssd-boot-raspberry-pi-5" rel="noreferrer"> Jeff's guide</a> on setting the boot order for the NVME- making sure you've done these items first:</p><ul>
<li>Installed Raspberry Pi OS on a microSD card - you don't need to keep your OS here (and I don't want this install permanently here anyway)</li>
<li>Follow Jeff's guide for changing boot order (<a href="https://www.jeffgeerling.com/blog/2023/nvme-ssd-boot-raspberry-pi-5">jeffgeerling.com</a>)</li>
<li>Image one of the NVME drives with Raspberry Pi OS - you will connect one of your new NVME drives using your NVME to USB adapter and image it using the Raspberry Pi Imager (<a href="https://www.raspberrypi.com/software/">raspberrypi.com</a>). <em><strong>WARNING- BE VERY CAREFUL NOT TO IMAGE AN EXISTING PARTITION ON YOUR PC WHEN YOU DO THIS.</strong></em></li>
<li>With the NVME drive imaged, put it back in your Pi along with the second blank one if you have it, and remove the microSD card.</li>
</ul>
<p>With all of those in place, you should be able to have a bootable Raspberry Pi system on your new NVME Quick Kit.  Here's where things get really fun, and how far you go will depend on how paranoid you want to be.  Here's a few simple concepts, assuming you are ultra-paranoid:</p><p><strong>Bare minimum install</strong> - don't install the desktop version of the OS and use the lite version.  Fewer packages installed reduces your OS vulnerability footprint.</p><p><strong>No external access</strong> - don't enable SSH, and in fact type this command and go through and turn off remote access (the exceptions are below):</p><blockquote>
<p>sudo raspi-config</p>
</blockquote>
<p><strong>Make sure SSH and anything related to remote access is turned off.</strong>  In my case I will only be using Ethernet, so I turn off bluetooth and wifi- these probably need to be set at boot too just in case.  We did just see an SSH vulnerability recently, and although it's a pretty well-audited package, I would never expose SSH to the Internet.  When we get to the file copies, you may need to turn it on, so read through the entire article to see what works for you.</p><p><strong>Change the default Pi password.  Seriously, go change it.</strong>  If you leave the default this entire project is kind of pointless.  Using a different account for the project is ideal too, but if SSH is turned off the default Pi account is probably fine.</p><p><strong>Be wary of where you store your Quick Kit.</strong>  This project scope doesn't cover encrypted volumes, and I did not manage to get a non-Pi OS working with this NVME hat, so your data is stored unencrypted on those NVME drives.  I want this, but you may not.</p><p><strong>Update your software! </strong> Especially if this is your first time installing the OS, run this command:</p><blockquote>
<p>sudo apt update &amp;&amp; sudo apt full-upgrade -y</p>
</blockquote>
<p>This command will update your Pi's apt (software library with an index of updates), then when it's successful (&amp;&amp;) download and update anything you have installed.  You can run this anytime to keep your machine up to date, but it needs an internet connection to do so.  When that's done we will need a tool called "rsync" and since it's sometimes on an install and sometimes not, you can always run:</p><blockquote>
<p>sudo apt install rsync</p>
</blockquote>
<p>This will install rsync and anything it needs to run.</p><p>Partition the second drive.  You really should run this before you put anything important since doing these steps wrong can wipe out your install disk.  This is not meant as an exhaustive guide to partitioning, and could cause significant data loss if not done correctly- so proceed on a test system that you can afford to lose data on.</p><p>First, we want to run "lsblk" to get our block ID's for the different disks.  Run the command:</p><blockquote>
<p>lsblk</p>
</blockquote>
<p>You will see something like this:</p><figure class="kg-card kg-image-card"><img src="/images/content/images/2024/09/image.png" class="kg-image" alt="" loading="lazy" width="485" height="114"></figure><p>I'm cheating a bit here, since the second disk has already been setup, but you see the nvme0n1, right?  It is very easy to get nvme1n1 and nvme0n1 mixed up, but 1n1 has our Pi install on it, and 0n1 is the one we want to partition.</p><p>Jeff Gerling has <a href="https://www.jeffgeerling.com/blog/2021/htgwa-partition-format-and-mount-large-disk-linux-parted" rel="noreferrer">just such an article</a> for setting up a partition for a new large drive in Linux- and it's worth a read here before continuing.  Seriously- do this step before you proceed, partitioning drives is risky for loss of existing data, even if you've done it before.</p><p>Now we have a reasonably setup NVME recovery kit, and the file backup from another host is pretty easy.  We're assuming your NVME Quick Kit has the SSH server turned off, so other hosts can't connect to your Quick Kit- but you can still connect to other hosts via SSH, and you can use rsync over SSH.  There are some limits though- Windows hosts don't have rsync installed by default, but you can probably find it or use WSL2, but getting ports on WSL2 exposed to the network is a bit of a pain- so if you want to copy to your Quick Kit from a Windows PC, you may need to enable SSH on your Quick Kit, and run the copy job on your PC.</p><p>With that out of the way, here's a script that is easy to read and edit for doing file copies:</p><pre><code>#!/usr/bin/bash

# Variables
REMOTE_USER="jay"
REMOTE_HOST="10.6.66.10"
# Remote folder is the folder location on the remote system 
# we will be copying over to the NVME Quick Kit
REMOTE_FOLDER="/home/jay"

# Local folder is the folder on the Quick Kit 
# where we will be copying the data to
LOCAL_BACKUP_DIR="/mnt/nvme2/_2024_host_backups"

# timestamp variable - this keeps us from overwriting 
# the last backup each time we run the command
TIMESTAMP=$(date +"%Y%m%d_%H%M")

# File name variable - you need to make sure you have the zip libraries installed locally for this to work
FILENAME="${REMOTE_HOST}_${TIMESTAMP}.zip"

# Create local backup directory if it does not exist
mkdir -p "$LOCAL_BACKUP_DIR"

# Sync remote folder to local machine
# note that /jay here is *under* the holder structure we are backing up
# you can add as many --exclude '/this/folder' arguments as you want here
# make sure both systems have rsync installed - this may be a challenge 
# for Windows PC's
rsync -avz --exclude '/jay/temp_cache' --exclude '/jay/other_folder' "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_FOLDER}" "$LOCAL_BACKUP_DIR/backup_temp"

# Zip the synced folder
cd "$LOCAL_BACKUP_DIR"
zip -r "$FILENAME" backup_temp

# Clean up temporary folder
rm -rf backup_temp

echo "Backup completed successfully. File: ${LOCAL_BACKUP_DIR}/${FILENAME}"
</code></pre>
<p>On your NVME Quick Kit you'll want to save this with a .sh extension to follow conventions, such as <em>backup.sh</em> and run this command to make it executable</p><blockquote>
<p>chmod +x backup.sh</p>
</blockquote>
<h3 id="hardware-limitations">Hardware Limitations</h3><p>The Pi 5 is probably the best Pi suited for a task like this, but there are some serious limitations.  First, rsync usually uses all available cores for copies, so the faster the Pi the better.  While you can run this on an older Pi with say, a USB hard drive, the throughput of both the Ethernet and a USB hard drive will probably not be quite what you'd expect for performance.  The limitation of a single 1Gbps Ethernet adapter while 2.5Gbps rolls out more commonly is a bit of a bottleneck too, but probably only in theory for what we're doing.</p><p>While this Pi has dual NVME drives, they are still sharing the single PCIE lane, so we're getting no where near the throughput that these drives are capable of- probably best too considering we're not doing much in the way of cooling for them.  Perhaps a new HAT will add a fan, and perhaps the Pi Foundation will add more lanes in the future?  I think we'll be waiting a bit, impatiently as usual.</p><p>Probably the biggest item that I found with this build was that none of my standard USB C adapters could power this sufficiently - unless I was using my Dell laptop 60W USB C power supply.  Not my little Anker, but it's a few years old and it may not be all the bricks themselves, but I can say with confidence all my older designs' USB C panel mounts can't handle the amps getting pulled by the Pi and two NVME drives.  That's why I ended up with the large port at the bottom, so I can easily pop out the display and plug directly into the Pi 5 itself.</p><p>Thank you for reading along!  My designs are available for paid subscribers, with the STL files requiring at least a month subscription.  Access to my CAD files lets you skip recreating the geometries yourself, and cost a fair bit more for my time.  I truly appreciate all my paid subscribers- thank you for sponsoring my work!  Your support lets me sidestep the shenanigans of influencer culture and paid promotion, letting me keep my voice to work on fun stuff.  Thank you!</p><h3 id="im-streaming-live-now">I'm Streaming Live Now</h3><p>I am now actively streaming on Twitch as well- doing some light Satisfactory gaming on Wednesdays, with CAD and Q&amp;A sessions on Tuesdays and Thursdays.  That schedule is subject to change, but you can find my profile here: <a href="https://www.twitch.tv/cheese_research">https://www.twitch.tv/cheese_research</a>.  Drop in on a stream and say hi!</p><h3 id="article-notes">Article Notes:</h3><p>These are the links from the article research that I did for this post:</p><p><strong>ServerFault</strong>- "wipefs" : <a href="https://serverfault.com/questions/250839/deleting-all-partitions-from-the-command-line">https://serverfault.com/questions/250839/deleting-all-partitions-from-the-command-line</a></p><p><strong>Jeff Geerling</strong> - Partitioning in Linux: <a href="https://www.jeffgeerling.com/blog/2021/htgwa-partition-format-and-mount-large-disk-linux-parted">https://www.jeffgeerling.com/blog/2021/htgwa-partition-format-and-mount-large-disk-linux-parted</a></p><p><strong>Jeff Geerling </strong>- NVME Boot on the Raspberry Pi 5: <a href="https://www.jeffgeerling.com/blog/2023/nvme-ssd-boot-raspberry-pi-5">https://www.jeffgeerling.com/blog/2023/nvme-ssd-boot-raspberry-pi-5</a></p><p>Distracted reading from the Cyberdeck Cafe Discord: <a href="https://apps.dtic.mil/sti/pdfs/ADA435835.pdf">https://apps.dtic.mil/sti/pdfs/ADA435835.pdf</a></p>
