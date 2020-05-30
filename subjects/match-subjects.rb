#  match-subjects.rb
#
#  Given a vocabulary TSV file of term/URI pairs (eg. LCSH),
#  and set of files containing terms (one per line),
#  find matching terms and generate TSV files containing term/URI pairs
#

require 'bundler/inline'

gemfile do
  source 'https://rubygems.org'
  gem 'pry'
end

tsv_file, *files = ARGV
abort 'ERROR: Please provide a TSV file' if tsv_file.nil? || tsv_file.empty?

exit if files.empty?
exit unless File.exist? tsv_file

# load TSV file into memory for searching
subjects = Hash.new

File.readlines(tsv_file).each do |line|
  fields = line.split("\t")

  # FIXME: this will overwrite duplicate hash keys!
  subjects[fields[1].strip] ||= fields[0]
end

# iterate over files matching pattern
files.each do |filename|
  # create a hash to hold the new subjects
  new_subjects = Hash.new

  # open file, iterate over subject strings
  File.readlines(filename).each do |line|
    # remove whitespace
    line.strip!

    # compact -- separator for LCSH
    line.gsub!(' -- ', '--')

    # skip empty lines
    next if line.empty?

    # search subject string in dictionary
    if dict = subjects[line]

      # write URI, string TSV to output
      new_subjects[dict] = line
    else

      # mint a URN using SHA sum
      new_subjects["<urn:rula:#{Digest::SHA256.hexdigest(line)}>"] = line

      # if this is a compound heading
      if line.include?('--')
        # walk backward until we find a matching subject
        heading = line.split('--')

        loop do
          heading.pop
          break if heading.empty?

          # add the subheading if it's in the dictionary
          subheading = heading.join('--')

          if dict = subjects[subheading]
            # write URI, string TSV to output
            new_subjects[dict] = subheading
            break
          end
        end
      end
    end

  end

  # create output file
  new_tsv = File.open("#{filename.chomp(File.extname(filename))}.tsv", "w")

  new_subjects.each do |uri, subject|
    new_tsv.puts "#{uri}\t#{subject}"
  end
end

exit