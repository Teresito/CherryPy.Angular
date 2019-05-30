import { HttpClient, HttpHeaders } from '@angular/common/http';
import { webServer } from '../constants';
import { Injectable } from '@angular/core';

@Injectable()
export class apiServices {

    private creds: String = btoa("tmag741:Teresito_419588351");
    
    private header = {
        headers: new HttpHeaders({
            'Authorization': 'Basic' + this.creds,
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*',
        })
    };
    // loginServer
    constructor(private httpClient: HttpClient) { }

    public pingAPI() {
        //console.log(this.creds);
        return this.httpClient.post(`${webServer}/ping`, null, this.header);
    }


}