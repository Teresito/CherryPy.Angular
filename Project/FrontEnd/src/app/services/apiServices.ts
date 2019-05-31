import { HttpClient, HttpHeaders } from '@angular/common/http';
import { webServer } from '../constants';
import { Injectable } from '@angular/core';

@Injectable()
export class apiServices {

    private creds: String = btoa("tmag741:Teresito_419588351");
    
    private httpOptions = { headers: new HttpHeaders({ 'Content-Type': 'application/json', }), responseType: 'text' as 'json' };

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
        //return this.httpClient.get('http://localhost:8080/',{ responseType: 'text' });
        //return this.httpClient.post('http://localhost:8080/', null, { responseType: 'text' });
        return this.httpClient.post('http://localhost:8080/', null, { responseType: 'json' });
    }


}