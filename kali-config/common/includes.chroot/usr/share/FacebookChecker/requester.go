package main

import (
	"errors"
	"io"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"github.com/pterm/pterm"
)

const (
	RESULT_DIR = "results"
)

// CookieJar is a CookieJar that will be used to store all the cookies
// that are added to it.
type CookieJar struct {
	cookies map[string][]*http.Cookie
}

// NewCookieJar creates a new CookieJar.
func NewCookieJar() *CookieJar {
	return &CookieJar{
		cookies: make(map[string][]*http.Cookie),
	}
}

// SetCookies handles the receipt of the cookies in a reply for the
// given URL.
func (jar *CookieJar) SetCookies(u *url.URL, cookies []*http.Cookie) {
	jar.cookies[u.Host] = cookies
}

// Cookies returns the cookies to send in a request for the given URL.
func (jar *CookieJar) Cookies(u *url.URL) []*http.Cookie {
	return jar.cookies[u.Host]
}

// User represents the result.
type User struct {
	Name           string
	ImageLink      string
	ImagePath      string
	EmailsOrPhones []string
}

// NewUser creates a new User.
func NewUser(name string, image string, emailsOrPhones []string) *User {
	return &User{
		Name:           name,
		ImageLink:      image,
		EmailsOrPhones: emailsOrPhones,
	}
}

// Request is a request to the server.
type Request struct {
	Client     *http.Client
	Parameters map[string]string
}

// NewRequest creates a new Request.
func NewRequest(client *http.Client) *Request {
	return &Request{
		Client: client,
	}
}

// Response is the response from the server.
type Response struct {
	StatusCode int
	Body       string
}

// NewResponse creates a new Response.
func NewResponse(statusCode int, body string) *Response {
	return &Response{
		StatusCode: statusCode,
		Body:       body,
	}
}

// Requester is to be used to make requests to the server.
type Requester struct {
	Input    string
	Request  *Request
	Response *Response
	User     *User
}

// NewRequester creates a new Requester.
func NewRequester(input string, request *Request) *Requester {
	return &Requester{
		Input:   input,
		Request: request,
	}
}

// Send GET request to the server.
func (r *Requester) GET(url *url.URL) {
	// send the request
	response, err := r.Request.Client.Get(url.String())
	if err != nil {
		panic(err)
	}

	// read the response
	defer response.Body.Close()
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		panic(err)
	}

	// set the response
	r.Response = NewResponse(response.StatusCode, string(body))
}

// Send POST request to the server.
func (r *Requester) POST(url *url.URL) {

	// create the form
	formData := url.Query()
	for key, value := range r.Request.Parameters {
		formData.Add(key, value)
	}

	// send the request
	response, err := r.Request.Client.Post(url.String(), "application/x-www-form-urlencoded", strings.NewReader(formData.Encode()))
	if err != nil {
		panic(err)
	}

	// read the response
	defer response.Body.Close()
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		panic(err)
	}

	// set the response
	r.Response = NewResponse(response.StatusCode, string(body))
}

// PrepareParameters prepares the parameters for the request.
func (r *Requester) PrepareParameters() {
	// read HTML document
	doc, err := goquery.NewDocumentFromReader(strings.NewReader(r.Response.Body))
	if err != nil {
		panic(err)
	}

	// extract the parameters
	lsd := doc.Find("input[name=lsd]").AttrOr("value", "LSD")
	jazoest := doc.Find("input[name=jazoest]").AttrOr("value", "JAZOEST")

	r.Request.Parameters = map[string]string{
		"lsd":        lsd,
		"jazoest":    jazoest,
		"email":      r.Input,
		"did_submit": "Search",
	}
}

// ExtractInformation extracts the information from the response.
func (r *Requester) ExtractInformation() {
	doc, err := goquery.NewDocumentFromReader(strings.NewReader(r.Response.Body))
	if err != nil {
		panic(err)
	}

	// extract the name
	Name := doc.Find("div[class='bb bc']").Text()

	// extract the image
	Image := doc.Find("img[class='x y l z']").AttrOr("src", "No IMAGE")

	// change the image to the full image
	image, _ := url.Parse(Image)
	values, _ := url.ParseQuery(image.RawQuery)
	values.Set("square_px", "500")
	image.RawQuery = values.Encode()
	Image = image.String()

	EmailsOrPhones := []string{}
	doc.Find("div[class='bk bl']").Each(func(i int, s *goquery.Selection) {
		EmailsOrPhones = append(EmailsOrPhones, s.Text())
	})

	if Name != "" {
		r.User = NewUser(Name, Image, EmailsOrPhones)
		// download the profile image
		err = r.DownloadImage()
		if err != nil {
			pterm.Warning.Println(err)

		}
	}

}

func (r *Requester) DownloadImage() error {
	//Get the response bytes from the url
	response, err := http.Get(r.User.ImageLink)
	if err != nil {
		return err
	}
	defer response.Body.Close()

	if response.StatusCode != 200 {
		return errors.New("received non 200 response code while downloading profile image")
	}

	// check if RESULT_DIR exists
	if _, err := os.Stat(RESULT_DIR); os.IsNotExist(err) {
		// create RESULT_DIR
		err = os.Mkdir(RESULT_DIR, 0755)
		if err != nil {
			return err
		}
	}

	// set the image path
	r.User.ImagePath = filepath.Join(RESULT_DIR, strings.ReplaceAll(r.User.Name, " ", "_")+".jpg")

	//Create a empty file
	file, err := os.Create(r.User.ImagePath)
	if err != nil {
		return err
	}
	defer file.Close()

	//Write the bytes to the fiel
	_, err = io.Copy(file, response.Body)
	if err != nil {
		return err
	}

	return nil
}
