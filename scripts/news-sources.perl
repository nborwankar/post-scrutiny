#!/usr/bin/perl -w
# 
# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/licenses/publicdomain/

my $file = $ARGV[0];
my $multiple_files = $ARGV[1] ? 1 : 0;

my %posters;
$posters{"news"} = {};
$posters{"mail"} = {};
$posters{"groups"} = {};

my %counts;
$counts{"news"} = 0;
$counts{"mail"} = 0;
$counts{"groups"} = 0;

my $type = "";
my $poster = "";

while (<>) {
  if ($_ =~ /^From: (.*)$/) {
    $poster = $1;
  }

  if ($_ =~ /^Injection-Info: /) {
    $type = "groups";
  }

  if ($_ =~ /^List-Id: /) {
    $type = "mail";
  }
  
  # Yes, this will miss off the last message. Use large sample sizes.
  # Patches welcome which don't make the code into the horrible mess of
  # repeating oneself which it became when I tried to change this. :-)
  if ($_ =~ /^From /) {
    if (!$type) {
      $type = "news";
    }
    
    if ($poster) {
      $posters{$type}->{$poster} = 1;
    }
    
    $counts{$type}++;
    $type = "";
    $poster = "";
  }
}

my $news = scalar(keys(%{$posters{"news"}}));
my $mail = scalar(keys(%{$posters{"mail"}}));
my $groups = scalar(keys(%{$posters{"groups"}}));
  
my $total = $mail + $groups + $news;

if ($total == 0) {
    print "No messages found.\n";
    exit;
}

if (!$multiple_files) {
    # If there's only one file on the command line, print its name
    print $file . "\n";
}

print "            Total   Web           Mail           News         \n";

print_line("Posters",
           $total,
           $groups,
           $mail,
           $news);

$total = $counts{'groups'} + $counts{'mail'} + $counts{'news'};

print_line("Posts",
           $total,
           $counts{'groups'},
           $counts{'mail'},
           $counts{'news'});

exit(0);


sub print_line {
    my ($label, $total, $groups, $mail, $news) = @_;
    printf("%10s: %5d ", $label, $total);
    print_figure($groups, $total);
    print_figure($mail, $total);
    print_figure($news, $total);
    print("\n");
}

sub print_figure {
    my ($number, $total) = @_;
    printf("%5d (%5.2f%%) ", $number, ($number / $total) * 100);
}

