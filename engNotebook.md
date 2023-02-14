# Adarsh + Andrew Design Notebook


## Horizontal Rules

___

---

***


## Typographic replacements

Enable typographer option to see result.

(c) (C) (r) (R) (tm) (TM) (p) (P) +-

test.. test... test..... test?..... test!....

!!!!!! ???? ,,  -- ---

"Smartypants, double quotes" and 'single quotes'


## Emphasis

**This is bold text**

__This is bold text__

*This is italic text*

_This is italic text_

~~Strikethrough~~


## Blockquotes


> Blockquotes can also be nested...
>> ...by using additional greater-than signs right next to each other...
> > > ...or with spaces between arrows.


## List of edge cases / modifications to consider:
+ Passing in IP address and port number through the command line. 
+ Handling too many arguments passed in through the command line. 
+ Handling spaces before and after the delimeter (will likely need to do strip())
+ Handling spaces before and after the operational keyword.
+ Testing what happens when two users try to log in at the same time or one user logs in when the other is active.
+ Sending messages to a deleted account. 
+ What if we create two clients from the same client and tried to have them message each other.
+ Do operations on UUIDs that don't exist.
+ Handling ill-formed regex strings
+ 
Unordered

+ Create a list by starting a line with `+`, `-`, or `*`
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
+ Very easy!

Ordered

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa


1. You can use sequential numbers...
1. ...or keep all the numbers as `1.`

Start numbering with offset:

57. foo
1. bar


## Code

Inline `code`