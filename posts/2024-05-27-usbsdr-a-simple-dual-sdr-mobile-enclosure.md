---
title: "USBSDR- A Dual SDR Mobile Enclosure"
date: 2024-05-27
slug: usbsdr-a-simple-dual-sdr-mobile-enclosure
tags: []
description: 
canonical_url: 
layout: post
---
<p>This time around I have a fairly easy project to build and print.  I needed a way to take two SDR dongles mobile, but heavy and unwieldy.  I was always a bit nervous about how much pressure the cables put on USB ports, especially on expensive laptops. </p><figure class="kg-card kg-image-card"><img src="__GHOST_URL__/content/images/2024/05/JAY00292-1.jpg" class="kg-image" alt="" loading="lazy" width="2000" height="1285" srcset="__GHOST_URL__/content/images/size/w600/2024/05/JAY00292-1.jpg 600w, __GHOST_URL__/content/images/size/w1000/2024/05/JAY00292-1.jpg 1000w, __GHOST_URL__/content/images/size/w1600/2024/05/JAY00292-1.jpg 1600w, __GHOST_URL__/content/images/2024/05/JAY00292-1.jpg 2000w" sizes="(min-width: 720px) 720px"></figure><p>My solution is pretty straightforward, two RTL-SDR USB dongles and a USB hub in a 3D printed enclosure.  It doesn't have to be carbon fiber filament, but I think it looks best and prints well for me.  The design is a top, bottom, and two ends.  The two ends are pretty easy to customize too. Eagle-eyed readers will notice the picture above has a little flex on that USB cable too- but this time it's going into a $30 USB hub instead of a much more expensive laptop.  Many USB ports have a bit of play to them as well, unless you go for expensive connectors.  This way you can give some abuse to this and just swap out the hub if needed.</p><p>The other big advantage to this case is that I have some venting, but more importantly space between the devices and the outside.  These SDR devices in general can get quite hot, this way I am a little less worried about the heat damaging something they sit next to.</p><figure class="kg-card kg-image-card"><img src="__GHOST_URL__/content/images/2024/05/JAY00293.jpg" class="kg-image" alt="" loading="lazy" width="2000" height="1224" srcset="__GHOST_URL__/content/images/size/w600/2024/05/JAY00293.jpg 600w, __GHOST_URL__/content/images/size/w1000/2024/05/JAY00293.jpg 1000w, __GHOST_URL__/content/images/size/w1600/2024/05/JAY00293.jpg 1600w, __GHOST_URL__/content/images/2024/05/JAY00293.jpg 2000w" sizes="(min-width: 720px) 720px"></figure><p>The whole thing is held together with a few metric flat head screws on the flat sides to keep it all flush, then with some socket head screws on the end.  The design is available for paid subscribers, both at the STL and CAD file levels.  As always, these subscriptions support these projects, so thank you to all of you for supporting my work.</p><figure class="kg-card kg-image-card"><img src="__GHOST_URL__/content/images/2024/05/JAY00296.jpg" class="kg-image" alt="" loading="lazy" width="2000" height="1132" srcset="__GHOST_URL__/content/images/size/w600/2024/05/JAY00296.jpg 600w, __GHOST_URL__/content/images/size/w1000/2024/05/JAY00296.jpg 1000w, __GHOST_URL__/content/images/size/w1600/2024/05/JAY00296.jpg 1600w, __GHOST_URL__/content/images/2024/05/JAY00296.jpg 2000w" sizes="(min-width: 720px) 720px"></figure><p>Finally, the ends have plenty of space for hand-tightening SMA connectors, as well as screwing in some BNC adapters, which work well with the <a href="https://zbm2industries.com/products/qp-whip-antenna-thicc" rel="noreferrer">ZBM2 antennas</a> (which are awesome).</p><p><strong>Design Files</strong></p><p>Paid STL subscribers have access to the binary STL files <a href="https://doscher.com/paid-subscribers-only-usbsdr-enclosure-stl-files" rel="noreferrer">here</a>. CAD Subscribers have access to the Fusion 360 source file <a href="https://doscher.com/cad-subscribers-only-usbsdr-enclosure-cad-files" rel="noreferrer">here</a>.</p><figure class="kg-card kg-image-card"><img src="__GHOST_URL__/content/images/2024/05/Sdrusb---Movie-V2---Published.gif" class="kg-image" alt="" loading="lazy" width="800" height="600" srcset="__GHOST_URL__/content/images/size/w600/2024/05/Sdrusb---Movie-V2---Published.gif 600w, __GHOST_URL__/content/images/2024/05/Sdrusb---Movie-V2---Published.gif 800w" sizes="(min-width: 720px) 720px"></figure><p><strong>Parts List</strong></p>
<ul>
<li>RTL SDR USB Adapter (v4 has been tested, but other revisions of the same brand may be OK) - <a href="https://amzn.to/4bAmMHg">Amazon</a></li>
<li>Startech USB Hub - <a href="https://amzn.to/3UVTlZ5">Amazon</a></li>
<li>USB B to USB C Cable - <a href="https://amzn.to/3KmTZda">Amazon</a></li>
<li>Velcro Ties - <a href="https://amzn.to/3wQmayd">Amazon</a></li>
</ul>
<p><strong>Update - I no longer recommend these hex drive flathead screws for the chassis- they are easily stripped.</strong></p>
<ul>
<li>M2.5x12mm Flathead Hex Drive Screws - <a href="https://www.mcmaster.com/91294A020/">McMaster Carr</a></li>
</ul>
<p><strong>Instead I recommend these philips head variants for the chassis:</strong></p>
<ul>
<li>M2.5x12mm Flathead Philips Head Screws - <a href="https://www.mcmaster.com/92010A022/">McMaster Carr</a></li>
</ul>
<p><strong>The endcap screws should be fine as hex drive, with the M4 size being pretty reliable from my experience.</strong></p>
<ul>
<li>M4x10mm Socket Head Screws for the Antenna End Cap - <a href="https://www.mcmaster.com/91290A144/">McMaster Carr</a></li>
<li>M4x20mm Screws for the USB End Cap (Flathead) - <a href="https://www.mcmaster.com/91294A196/">McMaster Carr</a></li>
<li>M4x20mm Screws for the USB End Cap (Socket Head) - <a href="https://www.mcmaster.com/91290A168/">McMaster Carr</a></li>
</ul>
