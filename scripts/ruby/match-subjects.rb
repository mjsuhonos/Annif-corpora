require 'bundler/inline'

gemfile do
  source 'https://rubygems.org'
  gem 'pry'
end

tsv_file, *files = ARGV

exit if files.empty?
exit if tsv_file.empty?
exit unless File.exist? tsv_file

# load TSV file into memory for searching
subjects = Hash.new

File.readlines(tsv_file).each do |line|
  fields = line.split("\t")
  subjects[fields[1].strip] ||= fields[0]
end

# iterate over files matching pattern
files.each do |filename|
  # create output file
  new_tsv = File.open("#{filename.chomp(File.extname(filename))}.tsv", "w")

  # open file, iterate over subject strings
  File.readlines(filename).each do |line|
    # remove whitespance and newlines
    line.strip!
    
    # search subject string in dictionary
    if dict = subjects[line]
      # write URI, string TSV to output
      new_tsv.puts "#{dict}\t#{line}"
    else
      # if not found, mint a URN using SHA sum
      new_tsv.puts "<urn:rula:#{Digest::SHA256.hexdigest(line)}>\t#{line}"
    end

  end

end

exit