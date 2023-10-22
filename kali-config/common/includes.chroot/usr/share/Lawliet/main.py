#!/usr/bin/python3
import requests
import os
from rich.console import Console
from rich.table import Table
import time
from rich.style import Style
from rich.progress import track
import sys
try:
	nome = sys.argv[1]
except Exception:
	print("Usage:\n\tlawliet.py username")
	exit()
green_bold = Style(color="green", blink=True, bold=True)
ascii_art = '''
   __               ___     __    
   / /  ___ __    __/ (_)__ / /_   
  / /__/ _ `/ |/|/ / / / -_) __/   
/____/\_,_/|__,__/_/_/\__/\__/                          
'''
os.system("clear")
link_list = []
console = Console()
console.print(ascii_art, justify="center", style="#D3869B bold")
console.print("[cyan]:: do not scroll up/down | all links will be saved in "+sys.argv[1]+".txt ::[cyan]\n", justify="center", end="")

tasks = [f"task {n}" for n in range(1, 3000)]
console.print("", justify="center", end="")

with console.status("[purple bold]", spinner = 'aesthetic') as status:
    while tasks:
        console.print("", justify="center", end="")
        task = tasks.pop(0)
        time.sleep(0.001)
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Find", style="dim", width=20, justify="center")
table.add_column("Url", style="dim", width=40, justify="center")

def site_check_y_n(url, minx, maxx, name_site):
	response = requests.get(url)
	if (len(response.text) >= minx):
		table.add_row(
		    "\n[green]"+name_site+"[green]\n",
		  	"\n"+url+"\n",
		)

		link_list.append(url)

	else:
		table.add_row(
		    "[red]"+name_site+"[red]\n",
		  	"-\n",
		)

	os.system("clear")
	console.print(ascii_art, justify="center", style="#D3869B bold")
	console.print(table, justify="center")

nome = sys.argv[1]
site_check_y_n(("https://instagram.com/"+nome),243566 , 200000, "Instagram")
try:
	site_check_y_n(("https://replit.com/@"+nome),200000 , 200000, "Repl.it")
except Exception:
	pass
try:
    site_check_y_n(("https://vsco.co/"+nome+"/gallery"),120000 , 120000, "Vsco")
except Exception:
    pass

try:
    site_check_y_n(("https://weheartit.com/"+nome),40500 , 40500, "Weheartit")
except Exception:
    pass

try:
    site_check_y_n(("https://www.younow.com/"+nome),11000 , 22000, "YouNow")
except Exception:
    pass

try:
    site_check_y_n_reverse(("https://imgsrc.ru/main/user.php?user="+nome),10000 , 22000, "imgsrc.ru")
except Exception:
    pass

try:
    site_check_y_n(("https://www.last.fm/user/"+nome),95000 , 90000, "last.fm")
except Exception:
    pass

try:
    site_check_y_n(("https://"+nome+".slack.com"),60000 , 60000, "Slack")
except Exception:
    pass

try:
    site_check_y_n(("https://fortnitetracker.com/profile/all/"+nome),150000 , 150000, "FortniteTracker")
except Exception:
    pass

try:
    site_check_y_n_reverse(("https://devrant.com/users/"+nome),30000 , 30000, "Devrant")
except Exception:
    pass

try:
    site_check_y_n(("https://trakt.tv/users/"+nome),100000 , 100000, "Trakt.tv")
except Exception:
    pass

try:
    site_check_y_n(("https://www.zoomit.ir/user/"+nome+"/"),10000 , 10000, "Zoomit")
except Exception:
    pass

try:
    site_check_y_n(("https://www.spletnik.ru/user/"+nome),300000 , 300000, "Spletnik")
except Exception:
    pass

try:
    site_check_y_n(("https://www.opennet.ru/~"+nome),10000 , 10000, "Opennet")
except Exception:
    pass

try:
    site_check_y_n(("https://career.habr.com/"+nome),32000 , 32000, "career.habr")
except Exception:
    pass

try:
    site_check_y_n(("https://mstdn.io/@"+nome),5000 , 5000, "mstdn.io")
except Exception:
    pass

try:
    site_check_y_n(("https://osu.ppy.sh/users/"+nome),110000 , 110000, "Osu")
except Exception:
    pass

try:
    site_check_y_n(("https://mastodon.cloud/@"+nome),5000 , 5000, "mastodon.cloud")
except Exception:
    pass

try:
    site_check_y_n(("https://promodj.com/"+nome),12000 , 12000, "Promodj")
except Exception:
    pass

try:
    site_check_y_n(("https://ok.ru/"+nome),10000 , 10000, "ok.ru")
except Exception:
    pass

try:
    site_check_y_n(("https://www.itemfix.com/c/"+nome),13900 , 13900, "Itemfix")
except Exception:
    pass

try:
    site_check_y_n(("https://www.keakr.com/en/profile/"+nome),170000 , 170000, "Keakr")
except Exception:
    pass

try:
    site_check_y_n(("https://www.myminifactory.com/users/"+nome),5000 , 5000, "Myminifactory")
except Exception:
    pass

try:
    site_check_y_n(("https://myanimelist.net/profile/"+nome),40000 , 40000, "Myanimelist")
except Exception:
    pass

try:
    site_check_y_n(("https://www.livelib.ru/reader/"+nome),20000 , 20000, "livelib.ru")
except Exception:
    pass

try:
    site_check_y_n(("https://www.kooapp.com/profile/"+nome),70000 , 70000, "Kooapp")
except Exception:
    pass

try:
    site_check_y_n(("https://www.spletnik.ru/user/"+nome),22000 , 22000, "spletnik.ru")
except Exception:
    pass

try:
    site_check_y_n(("https://dating.ru/"+nome),5000 , 5000, "dating.ru")
except Exception:
    pass

try:
    site_check_y_n_reverse(("https://www.dailykos.com/user/"+nome),30000 , 30000, "Dailykos")
except Exception:
    pass

try:
    site_check_y_n(("https://www.needrom.com/author/"+nome),5000 , 5000, "Needrom")
except Exception:
    pass

try:
    site_check_y_n(("https://"+nome+".newgrounds.com/"),27000 , 27000, "Newgrounds")
except Exception:
    pass

try:
    site_check_y_n(("https://notabug.org/"+nome),7000 , 7000, "Notabug")
except Exception:
    pass

try:
    site_check_y_n(("https://lobste.rs/u/"+nome),2200 , 2200, "lobste.rs")
except Exception:
    pass

try:
    site_check_y_n(("https://"+nome+".livejournal.com/"),10000 , 10000, "Livejournal")
except Exception:
    pass

try:
    site_check_y_n(("https://www.linux.org.ru/people/"+nome+"/profile"),5400 , 5400, "linux.org.ru")
except Exception:
    pass

try:
    site_check_y_n(("https://www.hackerearth.com/@"+nome),29000 , 29000, "Hackerearth")
except Exception:
    pass

try:
    site_check_y_n(("https://"+nome+".gumroad.com/"),2000 , 2000, "Gumroad")
except Exception:
    pass

try:
    site_check_y_n(("https://icq.im/"+nome),5200 , 5200, "icq.im")
except Exception:
    pass

try:
    site_check_y_n(("https://hubski.com/user/"+nome),2000 , 2000, "Hubski")
except Exception:
    pass

except Exception:
    pass

try:
    site_check_y_n(("https://asciinema.org/~"+nome),2000 , 2000, "Asciinema")
except Exception:
    pass

try:
    site_check_y_n(("https://anilist.co/user/"+nome),5000 , 5000, "anilist.co")
except Exception:
    pass

try:
    site_check_y_n(("https://archive.org/details/@"+nome),100000 , 100000, "Archive")
except Exception:
    pass

try:
    site_check_y_n(("https://developer.apple.com/forums/profile/"+nome),45000 , 45000, "AppleDev")
except Exception:
    pass

try:
    site_check_y_n(("https://discussions.apple.com/profile/"+nome),34000 , 34000, "AppleDiscussions")
except Exception:
    pass

try:
    site_check_y_n(("https://www.bikemap.net/en/u/"+nome),60000 , 60000, "Bikemap")
except Exception:
    pass

try:
    site_check_y_n_reverse(("https://bitbucket.org/"+nome),41000 , 41000, "Bitbucket")
except Exception:
    pass

try:
    site_check_y_n(("https://www.biggerpockets.com/users/"+nome),30000 , 30000, "Biggerpockets")
except Exception:
    pass

try:
    site_check_y_n(("https://bezuzyteczna.pl/uzytkownicy/"+nome),5000 , 5000, "Bezuzyteczna")
except Exception:
    pass

try:
    site_check_y_n(("https://f3.cool/"+nome),20000 , 20000, "f3.cool")
except Exception:
    pass

#site_check_y_n(("https://www.eyeem.com/u/"+nome),70000 , 70000, "Eyeem")
try:
    site_check_y_n(("https://www.enjin.com/profile/"+nome),40000 , 40000, "Enjin")
except Exception:
    pass

    site_check_y_n(("https://fameswap.com/user/"+nome),5000 , 5000, "Fameswap")
except Exception:
    pass

try:
    site_check_y_n(("https://genius.com/"+nome),100000 , 100000, "Genius")
except Exception:
    pass

try:
    site_check_y_n(("https://auth.geeksforgeeks.org/user/"+nome),50000 , 50000, "Geeksforgeeks")
except Exception:
    pass

try:
    site_check_y_n(("https://www.gamespot.com/profile/"+nome),50000 , 50000, "Gamespot")
except Exception:
    pass

try:
    site_check_y_n(("https://www.g2g.com/"+nome),5000 , 5000, "G2g")
except Exception:
    pass

try:
    site_check_y_n(("https://freesound.org/people/"+nome),8000 , 8000, "Freesound")
except Exception:
    pass

try:
    site_check_y_n(("https://www.discogs.com/user/"+nome),42000 , 42000, "Discogs")
except Exception:
    pass

try:
    site_check_y_n(("https://mastodon.xyz/@"+nome),10000 , 10000, "mastodon.xyz")
except Exception:
    pass

try:
    site_check_y_n(("https://www.mercadolibre.com.ve/perfil/"+nome),100000 , 100000, "Mercadolibre")
except Exception:
    pass

try:
    site_check_y_n(("https://www.interpals.net/"+nome),27000 , 27000, "Isnterpals")
except Exception:
    pass

try:
    site_check_y_n_reverse(("https://php.ru/forum/members/?username="+nome),50000 , 50000, "php.ru")
except Exception:
    pass

try:
    site_check_y_n(("https://www.shitpostbot.com/user/"+nome),10000 , 10000, "Shitpostbot")
except Exception:
    pass

try:
    site_check_y_n(("https://my.flightradar24.com/"+nome),10000 , 10000, "Flightradar24")
except Exception:
    pass

try:
    site_check_y_n(("https://fosstodon.org/@"+nome),10000 , 10000, "Fosstodon")
except Exception:
    pass

try:
    site_check_y_n(("https://hashnode.com/@"+nome),100000 , 100000, "Hashnode")
except Exception:
    pass

try:
    site_check_y_n_reverse(("https://bodyspace.bodybuilding.com/"+nome),150000 , 150000, "Bodybuilding")
except Exception:
    pass

try:
    site_check_y_n(("https://www.bookcrossing.com/mybookshelf/"+nome),25000 , 25000, "Bookcrossing")
except Exception:
    pass

try:
    site_check_y_n(("https://bezuzyteczna.pl/uzytkownicy/"+nome),10000 , 10000, "bezuzyteczna.pl")
except Exception:
    pass

try:
    site_check_y_n(("https://leetcode.com/"+nome),20000 , 20000, "Leetcode")
except Exception:
    pass

try:
    site_check_y_n_reverse(("https://hubpages.com/@"+nome),81000 , 81000, "Hubpages")
except Exception:
    pass

try:
    site_check_y_n(("https://app.memrise.com/user/"+nome),5000 , 5000, "Memrise")
except Exception:
    pass

try:
    site_check_y_n_reverse(("https://blog.naver.com/"+nome),2900 , 2900, "Naver")
except Exception:
    pass

try:
    site_check_y_n(("https://robertsspaceindustries.com/citizens/"+nome),61000 , 61000, "Robertsspaceindustries")
except Exception:
    pass

try:
    site_check_y_n(("https://www.sports.ru/profile/"+nome),310000 , 310000, "sports.ru")
except Exception:
    pass

try:
    site_check_y_n_reverse(("https://traktrain.com/"+nome),100000 , 100000, "Traktrain")
except Exception:
    pass

try:
    site_check_y_n(("https://www.shpock.com/shop/"+nome),110000 , 110000, "Shpock")
except Exception:
    pass

try:
    site_check_y_n(("https://trashbox.ru/users/"+nome),226000 , 226000, "trashbox.ru")
except Exception:
    pass

try:
    site_check_y_n(("https://vero.co/"+nome),7000 , 7000, "Vero")
except Exception:
    pass

try:
    site_check_y_n(("https://forum.velomania.ru/member.php?username="+nome),20000 , 20000, "Velomania")
except Exception:
    pass

try:
    site_check_y_n(("https://www.npmjs.com/~"+nome),24000 , 24000, "Npmjs")
except Exception:
    pass

try:
    site_check_y_n(("https://www.furaffinity.net/user/"+nome),5000 , 5000, "Furaffinity")
except Exception:
    pass

try:
    site_check_y_n_reverse(("https://www.behance.net/"+nome),250000 , 250000, "behance")
except Exception:
    pass

try:
    site_check_y_n(("https://blip.fm/"+nome),15000 , 15000, "blip.fm")
except Exception:
    pass

try:
    site_check_y_n(("https://www.airliners.net/user/"+nome+"/profile/photos"),10000 , 10000, "Airliners")
except Exception:
    pass

try:
    site_check_y_n(("https://social.tchncs.de/@"+nome),10000 , 10000, "tchncs.de")
except Exception:
    pass

try:
    site_check_y_n(("https://gfycat.com/@"+nome),36000 , 36000, "Gfycat")
except Exception:
    pass

try:
    site_check_y_n(("https://www.geocaching.com/p/default.aspx?u="+nome),6000 , 6000, "Geocaching")
except Exception:
    pass

try:
    site_check_y_n(("https://irecommend.ru/users/"+nome),70000 , 70000, "irecommend.ru")
except Exception:
    pass

try:
    site_check_y_n(("http://forum.igromania.ru/member.php?username="+nome),33000 , 33000, "igromania.ru")
except Exception:
    pass

try:
    site_check_y_n(("https://jbzd.com.pl/uzytkownik/"+nome),20000 , 20000, "Jbzd")
except Exception:
    pass

try:
    site_check_y_n(("https://www.wordnik.com/users/"+nome),47000 , 47000, "Wordnik")
except Exception:
    pass

try:
    site_check_y_n(("https://community.windy.com/user/"+nome),5000 , 5000, "Windy")
except Exception:
    pass

try:
    site_check_y_n(("https://hosted.weblate.org/user/"+nome),12000 , 12000, "Weblate")
except Exception:
    pass

try:
    site_check_y_n_reverse(("https://issuu.com/"+nome),50000 , 50000, "Issuu")
except Exception:
    pass

try:
    site_check_y_n(("https://www.instructables.com/member/"+nome),47000 , 47000, "Instructables")
except Exception:
            pass

try:
    site_check_y_n((f"https://etsy.com/people/{nome}"), 400000, 1000000, "Etsy")
except Exception:
    pass

try:
    site_check_y_n((f"https://twitter.com/{nome}"), 18000, 20000, "Twitter")
except Exception:
    pass

try:
    site_check_y_n((f"https://reddit.com/u/{nome}"), 200000, 300000, "Reddit")
except Exception:
    pass

try:
    site_check_y_n((f"https://github.com/{nome}"), 200000, 30000, "GitHub")
except Exception:
    pass


try:
    site_check_y_n((f"https://tumblr.com/{nome}"), 32000, 32000, "Tumblr")
except Exception:
    pass

# Duolingo does not return any response content size; would be in your best interest to check for profile existence differently

with open(nome+'.txt', 'w') as fp:
    for item in link_list:
        # write each item on a new line
        fp.write("%s\n" % item)

console.print("\n\n:: All link saved on"+nome+".txt ::", justify="center", style=green_bold)
