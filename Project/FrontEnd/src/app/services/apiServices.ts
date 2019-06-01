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
        return this.httpClient.post(`${webServer}/ping`, null, { responseType: 'json' });
    }

    public endpointAPI() {
        return this.httpClient.post(`${webServer}/endpoint`, {"a":"b"}, { responseType: 'text' });
    }

    public loginAPI(user: String, pass: String) {
        return this.httpClient.post(`${webServer}/login`, {"user":user, "pass":pass}, { responseType: 'text' });
    }

    public logoutAPI(){
        return this.httpClient.post(`${webServer}/logout`, { responseType: 'text' });
    }
    
    public checkPrivateData(){
        return this.httpClient.post(`${webServer}/check_privatedata`, null, { responseType: 'text' });
    }

    public newPrivateData(){
        return this.httpClient.post(`${webServer}/newPrivateData`, null, { responseType: 'text' });
    }

}