---
title: "Easy Laundry Notifications with Zigbee and Home Assistant"
date: 2023-10-26
slug: easy-laundry-notifications-with-zigbee-and-home-assistant
tags: []
description: 
canonical_url: 
layout: post
---
<p>I'll admit this is a pretty niche item, but if you're like me and have a set of stairs between you and your washer &amp; dryer, notifications are a huge help to minimize checking to see if laundry is done.  Luckily there's a pretty simple fix, and I'll go through it below.</p><p>First, thanks to <a href="https://hackaday.com/" rel="noreferrer">Hackaday </a>for posting a few other projects where people have taken different approaches.  There's the software approach, talking to the API of the washer and dryer, a good approach covered <a href="https://hackaday.com/2023/04/15/internet-of-washing-machines-solves-an-annoyance/" rel="noreferrer">here on Hackaday back in April</a>.  More recently, another maker took the hardware approach, making a power monitor from scratch, also covered <a href="https://hackaday.com/2023/10/20/spinning-up-a-new-laundry-monitor/" rel="noreferrer">here on Hackaday</a>.</p><p>Both approaches are inventive and great, but I had found an easier way last year, and didn't think it was worth a post until I saw the two above.  My approach is below, but simply it just requires two <a href="https://amzn.to/3S8yQJ2" rel="noreferrer">"Third Reality" smart switches</a> (the ones with power monitoring!) and a Home Assistant device with Zigbee.  <strong>Each power sensor plugs into the wall, and the washer and dryer each plug into their own smart switch- no wiring, soldering, or API coding needed.</strong></p><p>I have the <a href="https://www.home-assistant.io/yellow/" rel="noreferrer">Home Assistant Yellow</a>, one of many ways to add Zigbee to HA.  This will only work for 120V appliances that are within the spec of the smart switches- so 240V electric appliances definitely don't work.  Check the specs for your washer or dryer and make sure they are compatible with the smart switches.</p><blockquote><em>*I use affiliate links for the Amazon items in this post, which earns me a commission. This commission is a small percentage of the sale, and helps bit by bit to support the work on this site. *</em></blockquote><p>The premise is simple- when the washer power usage drops to a low baseline, it's idle.  When the dryer does the same thing, it's idle too.  Here's what my Home Assistant device info looks like for the washer's sensor:</p><figure class="kg-card kg-image-card"><img src="/images/content/images/2023/10/Power-Usage.jpg" class="kg-image" alt="" loading="lazy" width="664" height="587" srcset="/images/content/images/size/w600/2023/10/Power-Usage.jpg 600w, /images/content/images/2023/10/Power-Usage.jpg 664w"></figure><p>You can see the "active power" is at 1.5W, which is pretty low, and definitely means the washer isn't actively washing clothes.  The same approach can be taken for both the washer and the dryer, but your thresholds may be different.  I am using a gas dryer with a 120V plug, but an all-electric dryer may not work for this approach.</p><p>Here's where the automation kicks in- you will need a few automations.  I wanted to only know when <u>both</u> the washer and dryer are done.  Again, I will focus mostly on the washer code.</p><pre><code>alias: "Laundry: Washer Finished Notification"
description: ""
trigger:
  - type: power
    platform: device
    device_id: your_device_id
    entity_id: your_entity_id
    domain: sensor
    below: 5
    for:
      hours: 0
      minutes: 3
      seconds: 0
condition: []
action:
  - service: input_boolean.turn_on
    data: {}
    target:
      entity_id: input_boolean.laundry_washer_finished
mode: single</code></pre>
<p>Pretty simple so far- when the wattage read by the washer's wall plug drops below 5W, turn on the switch "input_boolean.laundry_washer_finished".  You will need to create your own custom switches in your config yaml.  You will want to do a similar automation for the dryer.  <u>Pay special attention to the duration- you want to make sure your washer is actually done, not just paused or between cycles.  3 minutes worked for me.</u></p><p>Finally, we create a rule to send a notification to our phones when <u>both</u> the washer and dryer wattage switches are "on", which indicates they are finished.  After the notification, we actually flip both switches back to off, reset for the next load of laundry.</p><pre><code>alias: Switch Out Laundry Notification
description: ""
trigger:
  - platform: time_pattern
    seconds: "30"
condition:
  - condition: and
    conditions:
      - condition: state
        entity_id: input_boolean.laundry_washer_finished
        state: "on"
      - condition: state
        entity_id: input_boolean.laundry_dryer_finished
        state: "on"
action:
  - service: notify.your_mobile_phone
    data:
      message: Switch Out Laundry
  - service: input_boolean.turn_off
    data: {}
    target:
      entity_id:
        - input_boolean.laundry_dryer_finished
        - input_boolean.laundry_washer_finished
mode: single</code></pre>
<p>Thanks for reading, and I hope this helps!  This has been working reliably for us for months.  Good luck, and happy hacking!  Thank you to <a href="https://hackaday.com/" rel="noreferrer">Hackaday </a>for sharing people's projects!</p>
