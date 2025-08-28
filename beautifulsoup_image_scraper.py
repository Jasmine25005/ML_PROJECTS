{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6c1694f7-8f5c-464c-8575-1fd76506250a",
   "metadata": {},
   "outputs": [],
   "source": [
    "#!pip install BeautifulSoup4"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7513b4e8-c900-4bde-87e0-621df94eff76",
   "metadata": {},
   "outputs": [],
   "source": [
    "from urllib.request import urlopen  # To open a URL\n",
    "from bs4 import BeautifulSoup  # For parsing the HTML content"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "42597c66-b031-42c0-9a70-9f375a7ed960",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 1: Open the URL and read the HTML content\n",
    "myurl = urlopen(\"https://www.artpal.com/buy/abstract/\").read()\n",
    "print(myurl)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "58c75a33-8c5b-4104-a451-eae0ff20d70f",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 2: Parse the HTML content using BeautifulSoup, specifying the parser\n",
    "thehtmlcode = BeautifulSoup(myurl, features=\"html.parser\")\n",
    "#Print the parsed HTML content\n",
    "print(thehtmlcode)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "53c348b9-d74a-4eb2-bbd8-a0b39d9ee321",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 3: Extract the content of the first anchor tag (<a>) found in the HTML\n",
    "text =thehtmlcode.a.contents # 'contents' will get the content inside the <a> tag\n",
    "print(text)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "611841b9-29bf-463d-9039-0a9e7256ad8b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 4: Extract and display the title of the webpage\n",
    "print(\"Title: \",thehtmlcode.title) # 'title' gets the content of the <title> tag"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2507e58c-5ed1-402a-bc8e-15fa8b9105c0",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 5: Display the entire body of the webpage\n",
    "print(\"Body: \",thehtmlcode.body) # 'body' gets the content of the <body> tag\n",
    "\n",
    "#This HTML snippet was identified by inspecting the structure of a web page and locating the div containing the \"Table of Content\". Extract the text of the 'table_of_content' div\n",
    "Categories = thehtmlcode.find('div', id='popupWrapper') # Get the text from the extracted div, removing extra whitespace\n",
    "if Categories:\n",
    "    toc_text = Categories.get_text(strip= True , separator=' \\n ')\n",
    "    print(\"Categories:\")\n",
    "    print(toc_text)\n",
    "else :\n",
    "    print(\"No 'table_of_content' found.\")\n",
    "\n",
    "#Step 6: #to get all of the links mentioned in a page\n",
    "for link in thehtmlcode.find_all('a'):\n",
    "    href = link.get('href')\n",
    "    if href:\n",
    "        print(href)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d58e1625-ff44-40db-8b7c-cb5baf07fa8b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Extract all image URLs\n",
    "images = thehtmlcode.find_all('img')\n",
    "for img in images:\n",
    "    print(img.get('src'))\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
