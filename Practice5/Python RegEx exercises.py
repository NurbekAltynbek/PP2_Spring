#1
import re

text = "abbb a ab abb aab"

pattern = r"ab*"

matches = re.findall(pattern, text)
print(matches)

#2
import re

text = "ab abb abbb abbbb"

pattern = r"ab{2,3}"

matches = re.findall(pattern, text)
print(matches)

#3
import re

text = "hello_world test_text Hello_world"

pattern = r"[a-z]+_[a-z]+"

matches = re.findall(pattern, text)
print(matches)

#4
import re

text = "Hello world Python Test"

pattern = r"[A-Z][a-z]+"

matches = re.findall(pattern, text)
print(matches)

#5
import re

text = "acb a123b ab axxxb"

pattern = r"a.*b"

matches = re.findall(pattern, text)
print(matches)

#6
import re

text = "Hello, world. Python is fun"

result = re.sub(r"[ ,\.]", ":", text)

print(result)

#7
import re

text = "hello_world_python"

result = re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)

print(result)

#8
import re

text = "HelloWorldPython"

result = re.split(r"(?=[A-Z])", text)

print(result)

#9
import re

text = "HelloWorldPython"

result = re.sub(r"([A-Z])", r" \1", text)

print(result.strip())

#10
import re

text = "helloWorldPython"

result = re.sub(r"([A-Z])", r"_\1", text).lower()

print(result)