---
title: "small Project: local DNS with bind9 and Raspberry Pi OS"
date: 2020-11-02
slug: work-local-dns
tags: []
description: 
canonical_url: 
layout: post
---
<p>With what looks like another Fall and Winter indoors, I’ll be doing projects that focus on projects that are easy to start and hopefully have what you need on hand without ordering anything.  While there are custom DNS packages like PiHole, they usually focus on aggressive filtering- something you may not need if you’re already using a good Ad Blocker like uBlock Origin.</p><p>With that said, here’s what you need for this project.  I have a Raspberry Pi 4 listed below, but slower ones will do OK- but your DNS server may be slower to respond and may slow down your web browsing.</p><ul><li>Raspberry Pi 4 (I’m using a 2GB model) - <a href="https://amzn.to/2TJrqMS">Amazon</a></li><li>Samsung Endurance MicroSD card - <a href="https://amzn.to/3ej9NNq">Amazon</a></li><li>My favorite USB C charger (I have several of these with a permanent home in my lab) - <a href="https://amzn.to/35Wncaz">Amazon</a></li><li>Steady State Coffee - support your local coffee roasters! (Nensebo Refisa is my favorite) - <a href="https://www.steadystateroasting.com/collections/roasted-coffee">Steady State</a></li><li>An Ethernet port for your Pi- I don’t recommend running a Pi DNS server over WiFi if you can help it.</li></ul><p>This is a morning project because this only takes a few minutes to get up and going,  You’ll be all set to do a ton of customization and I’ll have some links for further reading.  Here’s the goals of this project:</p><ul><li>Install and configure a basic BIND9 DNS server on your Raspberry Pi</li><li>Configure basic DNS server options</li><li>Configure a forward lookup zone</li><li>Configure a reverse-lookup zone</li></ul><p>So what is DNS?  Each computer, router, or server on the Internet has an IP address- and while they work pretty well, they’re not easy to remember.  We do a better job of remembering names, so all DNS does in the basic sense is translate a name to an IP address.  The DNS records that do this are “A” records or “Host” records.  There’s a handful of others, but let’s focus on A records for this tutorial.</p><p>First, let’s make sure you have Raspberry Pi OS (formerly Raspbian) installed on your Pi.  You can use either the Lite or Full version, but if you’re not going to keep a monitor connected you can do fine with the Lite version.  Follow the steps <a href="https://www.raspberrypi.org/downloads/raspberry-pi-os/">here</a> to image your Pi and come back when you’re done.</p><p>You’ll also need to set a static IP on your Raspberry Pi’s Ethernet port, which you can do using <a href="https://www.raspberrypi.org/documentation/configuration/tcpip/">this article</a>.  You need your Pi to have a set IP address since your desktop will be pointed to it for DNS.  If you change the IP address of the Pi, you will need to change the settings on your router or devices.</p><p>Once you have the static IP set, write it down, you’ll need it later.  Now we’re ready to install the required software on the Pi.  First, do a full update on the Pi using the command:</p><pre><code>sudo apt update &amp;&amp; sudo apt full-upgrade -y</code></pre><p>That will run the update of apt then update any packages before we proceed.  When that’s done, run this:</p><pre><code>sudo apt install bind9 bind9utils bind9-doc</code></pre><p>This command will install all the BIND9 related components and any dependencies it may require.  No reboot should be needed, but if you need to go brew a second cup of coffee this is a good stopping point.</p><p>Configure BIND9</p><p>There’s only a few flat files to configure but there’s almost an endless implication to each configuration.  I’ll be outlining what you need for an <em>internal</em> DNS server.  External DNS servers require much more in the way of configuration, security, and monitoring.  Please do not use this guide alone and expose your DNS server to the Internet.</p><p>The first file we’ll tackle is the “bind9” configuration file, which you can edit by typing:</p><pre><code>sudo nano /etc/default/bind9</code></pre><p>Edit it to add the “-4” so your entire file looks like the code block below.  Don’t worry about the lines starting with '“#”, those are comments.  Feel free to add notes to yourself here too, you probably won’t need to come back to this file for a while.</p><pre><code>#
# run resolvconf?
RESOLVCONF=no

# startup options for the server
OPTIONS="-u bind -4"</code></pre><p>All the “-4” does is tell your Pi to run over IPv4 only.   Next, we’ll go into some more detailed options in the file “/etc/bind/named.conf.options” by running:</p><pre><code>sudo nano /etc/bind/named.conf.options</code></pre><p>This should give you a mostly-empty file.  I’ll show you the sections and then the whole file in a minute.</p><pre><code>acl localclients {
        10.0.0.0/16;
        192.168.1.0/24;
        localhost;
        localnets;
};</code></pre><p>In the section above, we’re using an “access control list” or “acl” to limit who the DNS server can talk to.  While DNS requests can be spoofed (part of why this is still an internal-only DNS server), this acl limits what IP addresses are allowed to talk to your DNS server.  the localhost and localnets are default entries, leave them in- but the other two are examples you can remove or modify for your local network.  First, let’s look at 10.0.0.0/16:</p><ul><li>10.0.0.0/16 is a pretty big subnet- that’s 10.0.x.x where each octet with an X can be 0-255.  Now you may have multiple /24 subnets under the /16 and that’s OK- you don’t need to call out multiple subnets individually if you can cover them with a single subnet mask.  Don’t make it overly broad though- the /16 subnet is substantially more than a single Raspberry Pi can handle if it’s even remotely utilized.</li><li>192.168.1.0/24 is a much better and more reasonable example.  This acl entry means that all the IPs from 192.168.1.1-254 can talk to the DNS server.  A /24 annotation is pretty common for home networks, so if your computers at home have a subnet of 255.255.255.0, then the /24 is for you.  Make sure the network your client PCs will be on is included in the acl.</li></ul><p>With the acl out of the way, let’s go with some options.  I’ll simply provide the options below, and feel free to do some research on each of these.  I explain some of the common ones and leave out the complex ones:</p><pre><code>options {
        directory "/var/cache/bind";
        recursion yes;
        allow-query   ;
        //dnssec-enable yes;
        auth-nxdomain no;

        // If there is a firewall between you and nameservers you want
        // to talk to, you may need to fix the firewall to allow multiple
        // ports to talk.  See http://www.kb.cert.org/vuls/id/800113

        // If your ISP provided one or more IP addresses for stable
        // nameservers, you probably want to use them as forwarders.
        // Uncomment the following block, and insert the addresses replacing
        // the all-0's placeholder.

        forwarders {
                1.1.1.1;
                1.0.0.1;
                8.8.8.8;
        };

        //========================================================================
        // If BIND logs error messages about the root key being expired,
        // you will need to update your keys.  See https://www.isc.org/bind-keys
        //========================================================================
        dnssec-validation yes;

        listen-on-v6   ;
};</code></pre><p>Check the directory, recursion, and especially the allow-query items are added here if they aren’t by default.  The allow-query references “localclients” which is your acl name from the previous example.</p><p>Our little DNS server will let us set our own local DNS entries, but they will need to forward requests for anything they don’t have.  I have set the forward IPs to CloudFlare (1.1.1.1 and 1.0.0.1) and Google (8.8.8.8) but you can put in any DNS servers you want here.</p><p>I’ll link to more about dnssec but make sure you include all the options in this config.  Here’s the complete config below:</p><pre><code>acl localclients {
        10.0.0.0/16;
        192.168.1.0/24;
        localhost;
        localnets;
};
options {
        directory "/var/cache/bind";
        recursion yes;
        allow-query   ;
        //dnssec-enable yes;
        auth-nxdomain no;

        // If there is a firewall between you and nameservers you want
        // to talk to, you may need to fix the firewall to allow multiple
        // ports to talk.  See http://www.kb.cert.org/vuls/id/800113

        // If your ISP provided one or more IP addresses for stable
        // nameservers, you probably want to use them as forwarders.
        // Uncomment the following block, and insert the addresses replacing
        // the all-0's placeholder.

        forwarders {
                1.1.1.1;
                1.0.0.1;
                8.8.8.8;
        };

        //========================================================================
        // If BIND logs error messages about the root key being expired,
        // you will need to update your keys.  See https://www.isc.org/bind-keys
        //========================================================================
        dnssec-validation yes;

        listen-on-v6   ;
};</code></pre><p>BIND can be pretty picky about syntax, so to make sure it’s OK with everything so far, run this:</p><pre><code>sudo named-checkconf</code></pre><p>This will check your config and tell you if there are any errors.  This is helpful if you need to make a bunch of changes, you can run this as you go.  With the BIND9 options done, now we need to do the local DNS configuration.  This is a little weird to split up the config for small settings, but in larger deployments this makes more sense.  Next we run:</p><pre><code>sudo nano /etc/bind/named.conf.local</code></pre><p>Here’s the whole sample, this time I will explain what each section does:</p><pre><code>//
// Do any local configuration here
//

// Consider adding the 1918 zones here, if they are not used in your
// organization
//include "/etc/bind/zones.rfc1918";

zone "back7.co" {
    type master;
    file "/etc/bind/zones/db.back7.co"; # zone file path
    allow-transfer   ;           # ns2 private IP address - secondary
};

zone "168.192.in-addr.arpa" {
    type master;
    file "/etc/bind/zones/db.192.168";  # 192/168.0.0/16 subnet
    allow-transfer   ;  # ns2 private IP address - secondary
};</code></pre><p>This file tells BIND where the “zone” file is for each zone.  There’s a forward lookup zone that translates DNS names to IP addresses, and an optional reverse lookup that maps IP addresses to DNS names.</p><p>For the example of “back7.co” in the zone name, that’s the DNS name of your DNS zone- this can be a domain you own, or a private domain like “lab.local” but beware- nonexistent DNS names like those ending in .local can’t use commercial encryption certificates.  Note the file path- we’re going to create the zone files in a bit, but take note for now.  For yours, if your DNS zone is hackthegibson.com, then make your file /etc/bind/zones/db.hackthegibson.com.</p><p>I advise that if you’re worried about all of your Internet DNS going through one Raspberry Pi, then do this for two!  This can be confusing if you do them all at once, but the allow-transfer simply allows specific IP addresses to do “zone transfers” to keep them in sync.  192.168.1.3 is the IP address of “ns2” or the second PI.  All the config cares about is the IP address here- the stuff after the “#” is just a comment.</p><p>Does it make sense so far?  This so far is the config that points BIND to the “forward” lookup file that will map hostnames to IP addresses.  Before we edit that, we need to reference the optional “reverse lookup” zone.</p><p>The reverse lookup zone does some stuff that’s a little funky, so some of the octets from the IP range are actually inverted from what you may expect- pay special attention there.  The zone still maps back to a file “/etc/bind/zones/db.192.168” and you still need to specify any other DNS servers that are allowed to do full zone transfers.  Client computers do not need to do zone transfers!  Other than the zone which has “168.192” in the name, it’s very similar to the forward lookup reference.  Let’s say you wanted the reverse zone for the 10.1.2.0 subnet, you’d need to call the zone “2.1.10.in-addr.arpa” with the subnet reversed.  This is also a great source to read up on if you’re bored or just want to learn more.</p><p>Go ahead and save and close the file- pay special attention to the formatting and the file paths- everything needs to be perfect in the config files.  Now let’s make the zones directory with this command:</p><pre><code>sudo mkdir /etc/bind/zones</code></pre><p>This will be the folder that holds our zone configuration files.  Next, let’s edit the forward lookup file by running:</p><pre><code>/etc/bind/zones/db.back7.co</code></pre><p>You’ll get an empty file, let’s put this in there for a sample:</p><pre><code>;
; BIND data file for local loopback interface
;
$TTL    604800
@       IN      SOA     ns1.back7.co. admin.back7.co. (
                              9         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
; name servers - NS records
        IN      NS      dns1.back7.co.
        IN      NS      dns2.back7.co.

; name servers - A records
dns1.back7.co.               IN      A       192.168.1.2
dns2.back7.co.               IN      A       192.168.1.3

; 192.168.0.0/16 - A records
router.back7.co.             IN      A       192.168.1.1
www.back7.co.                IN      A       192.168.1.4</code></pre><p>The SOA record at the top needs to have your server’s DNS name (this example is ns1.back7.co.) and the admin contact is admin.back7.co.  Make sure to include the “.” after each .com or .co, etc. for DNS config.</p><p>Now here’s the fun part- the “Serial” number needs to be increased each time you edit the file.  It’s usually easiest to increase it to the next odd number.  Right now it’s 9, next time you make changes make sure you set it to 11.  Without this, BIND will not re-read changes to the file.  The Refresh, Retry, Expire, and Negative Cache TTL are all in seconds, the defaults are fine for most people most of the time.</p><p>Next you see the records with a “;” for comments.  Go ahead and use tabs to keep it easy to read, but you can see I first create “NS” records, which are my name servers of ns1.back7.co and ns2.back7.co.  We’ll assign them to IP addresses, but for now we are telling BIND these two servers are the authority for this domain.</p><p>Next you can see A records.  Feel free to edit/modify the names, but they have to be in the same DNS zone as the one specified for the file.  You can’t put an acme.com record in the back7.co zone.  When you have all your records, go ahead and save then close the file.</p><p>Next let’s go ahead and make the reverse lookup file:</p><pre><code>sudo nano /etc/bind/zones/db.192.168</code></pre><p>Now here’s the deal with reverse- it may seem really cool to use these for everything, and there are good reasons to do this- but remember that a wrong record is worse than an empty one, so if you put a ton of entries in here make sure to maintain them.  Because of this, let’s only put the router in:</p><pre><code>;
; BIND reverse data file for local loopback interface
;
$TTL    604800
@       IN      SOA     dns1.back7.co. admin.back7.co. (
                              3         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;

; name servers - NS records
      IN      NS      dns1.back7.co.
      IN      NS      dns2.back7.co.
      
; PTR Records
1.1   IN      PTR     router.doscher.com.    ; 192.168.1.1</code></pre><p>You still need to increment the Serial each time you edit it (this is the case for any zone file) and you still need to specify the DNS servers (NS or nameservers) via those same entries.  Finally, you can create the reverse lookup record, or “PTR” aka “Pointer” record.  Now here’s where 1.1 isn’t helpful- the router is 192.168.1.1, but for reverse records are backwards here based on how lookups are done- so if the router was 192.168.1.5, the PTR record would be “5.1”.</p><p>It’s OK to leave the file without any PTR records too, but since this was referenced in the other configs it at least needs most of the file.  Once you save and close, you can restart BIND with the following command:</p><pre><code>sudo systemctl restart bind9</code></pre><p>Remember you can run “sudo named-checkconf” to check your configs as well.  From there you now have a basic DNS server.  You’re probably out of coffee by now too, so here are some things for future projects on your network:</p><ul><li>Create a second DNS server and allow zone transfers for each domain between them.</li><li>Set them as primary and secondary DNS servers on your PC first to test, and if all goes well you can set these as the DNS servers for your DHCP server (usually on your router).</li><li>I don’t recommend using these DNS servers to be exposed to the Internet because of risks of DNS amplification/DDoS.</li><li>I don’t recommend using these as DNS servers for your router itself- use the ones from your ISP or CloudFlare, etc.</li><li>Let me know in the comments if you spot a bug or mistake!  Thanks for reading!</li></ul>
