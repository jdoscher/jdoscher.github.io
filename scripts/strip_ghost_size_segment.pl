#!/usr/bin/env perl
use strict; use warnings;
local $/ = undef;

# Gather files from git (falls back to walking tree)
my @files = `git ls-files`;
if ($? != 0) {
  @files = qx(find posts pages _layouts _includes -type f \\( -name '*.md' -o -name '*.markdown' -o -name '*.html' \\));
}

my $changed = 0;
for my $f (@files) {
  chomp $f;
  next unless $f =~ /\.(md|markdown|html)$/i;
  next if $f =~ m{^_site/};

  open my $in, '<:raw', $f or next;
  my $s = do { local $/; <$in> };
  close $in;
  my $orig = $s;

  # Strip Ghost responsive segment: content/images/size/w####/ → content/images/
  # (works for absolute, protocol-relative, local, and already-rewritten /images/... paths)
  $s =~ s{(/images)?/content/images/size/w\d+/}{$1 . "/content/images/"}ge;

  # Also handle plain (not prefixed) /content/images/size/w####/
  $s =~ s{(?<![a-zA-Z])/content/images/size/w\d+/}{/content/images/}g;

  # Escaped variants inside code blocks: content\/images\/size\/w####\/
  $s =~ s{content\\/images\\/size\\/w\d+\\/}{content\\/images\\/}g;

  if ($s ne $orig) {
    open my $out, '>:raw', $f or die "write $f: $!";
    print $out $s;
    close $out;
    print "Rewrote $    print "+$changed;
  }
}
print "Done. Changed $changed file(s).\n";
