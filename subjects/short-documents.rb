require 'bundler/inline'

gemfile do
  source 'https://rubygems.org'
  gem 'pry'
end

*tsv_files = ARGV
exit if tsv_files.empty?

# iterate over files matching pattern
tsv_files.each do |filename|

  # load TSV file, extract URIs
  subject_uris = File.readlines(filename).map {|line| line.split("\t").first }.sort
  
  # load title file
  title_name = "../titles/#{filename.chomp(File.extname(filename))}.txt"
  abstract_name = "../abstracts/#{filename.chomp(File.extname(filename))}.txt"
  
  if File.exists? title_name
    short_text = File.read(title_name).strip

    if File.exists? abstract_name
      short_text << ' -- ' + File.read(abstract_name).strip
    end
    short_text.delete! "\n\r\t"

    new_tsv = File.open("../short/#{filename.chomp(File.extname(filename))}.tsv", "w")
    new_tsv.puts ([short_text] + subject_uris).join("\t")
    new_tsv.close
  else
    puts "ERROR: no title for #{filename}"

  end
end

exit