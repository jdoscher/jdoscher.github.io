#!/usr/bin/env perl
use strict; use warnings;
local $/ = undef;

# Collect candidate files from git (fallback to tree if needed)
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

  # Replace any form of Ghost image URLs with local /images/content/images/
  $s =~ s{__GHOST_URL__/content/images/}{/images/content/images/}gi;
  $s =~ s{https?://(?:www\.)?doscher\.(?:net|com)/content/images/}{/images/content/images/}gi;
  $s =~ s{//(?:www\.)?doscher\.(?:net|com)/content/images/}{/images/content/images/}gi;

  # Bare '/content/images/' preceded by a delimiter-like char -> fix path
  $s =~ s{(^|[\(\[\{\s"'`])(/content/images/)}{$1 . "/images/content/images/"}ge;

  # Escaped URLs inside code blocks (https:\/\/...\/content\/images\/...)
  $s =~ s{https:\\/\\/(?:www\\.)?doscher\\.(?:net|com)\\/content\\/images\\/}{/images/content/images/}gi;

  if ($s ne $orig) {
    open my $out, '>:raw', $f or die "write $f: $!";
    print $out $s;
    close $out;
    print "Rewrote $f\n";
    ++$changed;
  }
}

print "Done. Changed $changed file(s).\n";
