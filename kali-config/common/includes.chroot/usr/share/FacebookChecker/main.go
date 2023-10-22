package main

import (
	"flag"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"sync"
	"time"

	"github.com/charmbracelet/lipgloss"
	"github.com/pterm/pterm"
)

var (
	// flag vars
	Input string
	// url vars
	URL, _      = url.Parse("https://mbasic.facebook.com/login/identify/?ctx=recover&search_attempts=0&alternate_search=0&toggle_search_mode=0")
	VIEW_URL, _ = url.Parse("https://mbasic.facebook.com/recover/initiate/?c=%2Flogin%2F&fl=initiate_view&ctx=msite_initiate_view")
	// style vars
	devlopedByStyle = lipgloss.NewStyle().Bold(true).
			Align(lipgloss.Center).
			Blink(true).Render
)

func init() {
	pterm.Println()
	str := pterm.DefaultHeader.WithBackgroundStyle(pterm.NewStyle(pterm.BgRed)).WithMargin(10).Sprintf(
		"FBC - Facebook Checker")

	pterm.DefaultCenter.Print(str)

	pterm.DefaultCenter.WithCenterEachLineSeparately().Printf(
		fmt.Sprintf("Created by %v - (%v)\n%s[%s]%s", pterm.LightRed(devlopedByStyle("Yasser JANAH")), pterm.Green(devlopedByStyle("th3x0ne")), pterm.Yellow("contact"), pterm.Cyan("at"), pterm.Yellow("yasser-janah.com")))

	pterm.DefaultCenter.WithCenterEachLineSeparately().Printf("-----------------\n")

	// flags
	flag.StringVar(&Input, "id", "", "target email/user")
	flag.Parse()

	if Input == "" {
		pterm.Warning.Println("Please specify -id")
		os.Exit(1)
	}
}

var rs chan *Requester = make(chan *Requester)

func main() {

	var wg sync.WaitGroup

	mainSpinner, _ := pterm.DefaultSpinner.Start(fmt.Sprintf("Searching %v ...", pterm.Yellow(Input)))

	go func(requester *Requester, wg *sync.WaitGroup) {
		Worker(requester, wg)
	}(NewRequester(Input, NewRequest(&http.Client{
		Jar:     NewCookieJar(),
		Timeout: time.Duration(time.Second * 10),
	})), &wg)

	wg.Wait()

	r := <-rs

	mainSpinner.UpdateText(fmt.Sprintf("Searching %v ... %s", pterm.Yellow(Input), pterm.Green("Done")))
	mainSpinner.Stop()
	pterm.Println()

	if r.User != nil {
		pterm.Printfln("[%s] Name : %s", pterm.Green("+"), pterm.Green(r.User.Name))
		pterm.Printfln("[%s] Image saved : %s", pterm.Green("+"), pterm.Green(r.User.ImagePath))
		pterm.Printfln("[%s] Emails or numbers associated with the account : ", pterm.Green("+"))
		for _, email := range r.User.EmailsOrPhones {
			pterm.Printfln("\t %s %s", pterm.White("•"), pterm.Green(email))
		}
	} else {
		mainSpinner.Fail("No account associated with " + pterm.Yellow(Input))
	}
}

func Worker(requester *Requester, wg *sync.WaitGroup) {
	wg.Add(1)
	requester.GET(URL)
	requester.PrepareParameters()
	requester.POST(URL)
	requester.GET(VIEW_URL)
	requester.ExtractInformation()
	rs <- requester
	wg.Done()
}
