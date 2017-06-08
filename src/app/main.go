package main

import (
	"app/settings"
	"app/views"
	"fmt"
	"log"
	"net/http"
)

func main() {
	//Load settings
	confs := settings.Setting{}
	confs = settings.Load()
	//Set URLs
	http.HandleFunc(confs.Home, views.Index)
	http.HandleFunc(confs.StaticDir, func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, r.URL.Path[1:])
	})
	http.HandleFunc("/submit/", views.Sub)
	http.HandleFunc("/images/", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "../"+r.URL.Path[1:])
	})
	http.HandleFunc("/result/", views.ResultRender)
	//Start the server
	fmt.Println("Server running on : " + confs.Host + confs.Port)
	serverErr := http.ListenAndServe(confs.Port, nil)
	if serverErr != nil {
		fmt.Println("Server error :\n")
		log.Fatal(serverErr)
	}
}
