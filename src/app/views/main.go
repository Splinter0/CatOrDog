package views

import (
	"app/settings"
	"crypto/md5"
	"fmt"
	"html/template"
	"io"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"
)

//A struct for the context in the page
type Context struct {
	ImagePath string
	Title     string
	StaticDir string
	Result    string
	Token     string
}

//A struct for the tokens
type Token struct {
	Token string
	Used  bool
}

//A struct for the results from the neural network
type Result struct {
	Token  string
	Result string
}

//Slice containing the results
var results []Result

//Slice containing the tokens
var tokens []Token

//Prepare for settings
var confs settings.Setting

//Index : the main page
func Index(w http.ResponseWriter, r *http.Request) {
	//Load settings
	confs = settings.Load()
	if r.Method != "GET" {
		http.Redirect(w, r, confs.Home, http.StatusMovedPermanently)
	} else {
		//Create the Token
		crutime := time.Now().Unix()
		h := md5.New()
		io.WriteString(h, strconv.FormatInt(crutime, 10))
		token := Token{
			Token: fmt.Sprintf("%x", h.Sum(nil)),
			Used:  false}
		//Add token to the tokens
		tokens = append(tokens, token)
		context := Context{
			Token:     token.Token,
			Title:     "Cat Or Dog - Home",
			StaticDir: confs.StaticDir,
		}
		t, _ := template.ParseFiles("templates/index.html")
		t.Execute(w, context)
	}
}

func Sub(w http.ResponseWriter, r *http.Request) {
	confs = settings.Load()
	if r.Method != "POST" {
		http.Redirect(w, r, confs.Home, http.StatusMovedPermanently)
	} else {
		r.ParseMultipartForm(32 << 20)
		//Create the token from the form
		token := Token{
			Token: r.Form.Get("token"),
			Used:  true}
		validToken := true
		//Token checking
		var tokenPointer int
		for i, t := range tokens {
			//Check if token is present in tokens
			if t.Token == token.Token {
				//Check is the token has been already used
				if !t.Used {
					validToken = true
				} else {
					http.Redirect(w, r, confs.Home, http.StatusMovedPermanently)
					validToken = false
				}
				tokenPointer = i
				break
			} else {
				validToken = false
			}
		}
		if validToken {
			//Load the file
			file, handler, err := r.FormFile("uploadfile")
			if err != nil {
				fmt.Println(err)
			}
			//Create filename using token
			fileName := strings.Split(handler.Filename, ".")[1]
			fileName = token.Token + "." + fileName
			//Write the file
			f, err := os.OpenFile("../images/"+fileName, os.O_WRONLY|os.O_CREATE, 0666)
			if err != nil {
				fmt.Println(err)
			}
			defer f.Close()
			io.Copy(f, file)
			//Wait until the neural network sends
			//a request, the result added in the slice
			result := "default"
			for {
				for _, r := range results {
					if r.Token == token.Token {
						//Get the result if the token matches
						result = r.Result
						break
					}
				}
				if result != "default" {
					break
				}
			}
			context := Context{
				ImagePath: "/images/" + fileName,
				Title:     "Cat Or Dog - Home",
				StaticDir: confs.StaticDir,
				Result:    result,
			}
			fmt.Println(result)
			t, _ := template.ParseFiles("templates/output.html")
			t.Execute(w, context)
			tokens[tokenPointer] = tokens[len(tokens)-1]
			tokens = tokens[:len(tokens)-1]
		}
	}
}

func ResultRender(w http.ResponseWriter, r *http.Request) {
	//Get the path
	path := r.URL.Path[len("/result/"):]
	//Get the token from the path
	token := strings.Split(path, "&")[0]
	//Iterate through the tokens
	for _, t := range tokens {
		if token == t.Token {
			//If token matches get the result from the path
			result := strings.Split(path, "&")[1]
			//Create a Result
			resultStruct := Result{
				Token:  token,
				Result: result,
			}
			//Add the result to the results (slice)
			results = append(results, resultStruct)
			return
		}
	}
	http.Redirect(w, r, confs.Home, http.StatusMovedPermanently)
}
