package settings

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
)

const settingsFile = "settings/settings.json"

//Setting : settings struct for the application
type Setting struct {
	Host      string
	Port      string
	Home      string
	StaticDir string
}

//Load application settings from settingsFile
func Load() Setting {
	confs := Setting{}
	data, _ := ioutil.ReadFile(settingsFile)
	settingsError := json.Unmarshal(data, &confs)
	if settingsError != nil {
		fmt.Println("Settings error :")
		log.Fatal(settingsError)
	}
	return confs
}
