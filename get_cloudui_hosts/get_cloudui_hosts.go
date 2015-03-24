package main

import (
    "fmt"
    "net/http"
    "io/ioutil"
    "os"
    "crypto/tls"
    "encoding/json"
    "flag"
    )

func main() {
    // from: http://mervine.net/json2struct
    type Cloudui_Hosts struct {
        CloudstackID string  `json:"cloudstack_id"`
        ClusterKey   string  `json:"cluster_key"`
        CreationDate string  `json:"creation_date"`
        Environment  string  `json:"environment"`
        Hostname     string  `json:"hostname"`
        ID           float64 `json:"id"`
        Owner        string  `json:"owner"`
        Product      string  `json:"product"`
        Release      string  `json:"release"`
        Tags         string  `json:"tags"`
    }

    server := flag.String("server", "https://cloudui.vast.com", "Cloudui hosts api url")
    hostname := flag.String("h", "unset", "hostname to look up")
    cluster := flag.Bool("c", false, "Print cluster membership?")
    flag.Parse()

    var serverstring string

    if *hostname != "unset" {
        serverstring = *server + "/api/hostdetails/" + *hostname
    } else {
        serverstring = *server + "/api/hosts"
    }

    // accept unsigned certs
    tr := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify : true},
    }
    client := &http.Client{Transport: tr}
    resp, err := client.Get(serverstring)

    // load json data from body
    jsonDataFromHttp, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Printf("%s", err)
        os.Exit(1)
    } 

    // unmarshal json object into array
    var jsonData []Cloudui_Hosts
    err = json.Unmarshal([]byte(jsonDataFromHttp), &jsonData) // here!
    if err != nil {
        fmt.Printf("%s", err)
        os.Exit(1)
    }

    // print hostname and cluster key
    if *hostname != "unset" {
        indented, err := json.MarshalIndent(jsonData, "", "\t")
        if err != nil {
            fmt.Println("error:", err)
        }
        fmt.Printf("%s\n", indented)
    } else {
        for i := range jsonData {
            if *cluster {
                fmt.Printf("%s - %s\n", jsonData[i].Hostname, jsonData[i].ClusterKey)
            } else {
                fmt.Printf("%s\n", jsonData[i].Hostname)
            }
        }
    }
}