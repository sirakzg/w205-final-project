using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NetworkManager : MonoBehaviour
{
    /* Implements a class to support following API calls
     * 
     *  docker-compose exec mids curl -X POST -H "Content-Type: application/json" -d '{"username":"test"}' http://localhost:5000/create_user
        docker-compose exec mids curl -X POST -H "Content-Type: application/json" -d '{"username":"test"}' http://localhost:5000/purchase_a_sword
        docker-compose exec mids curl -X POST -H "Content-Type: application/json" -d '{"username":"test"}' http://localhost:5000/purchase_an_axe
        docker-compose exec mids curl -X POST -H "Content-Type: application/json" -d '{"username":"test", "guild_type":2}' http://localhost:5000/join_guild
        ... '{"username":"test", "guild_type":2, "level":2, "weapon_type":"sword", "gold":200, "num_kills":10}' http://localhost:5000/player_died
    */

    public static NetworkManager _instance;
    private const string API_SERVER = "http://35.233.175.80:5000/";

    private Dictionary<string, string> headers;

    // Start is called before the first frame update
    void Awake()
    {
        // enforce one instance of class per scene
        if (_instance == null)
            _instance = this;
        else return;

        headers = new Dictionary<string, string>();
        headers.Add("Content-Type", "application/json");
    }

    // Update is called once per frame
    void Update()
    {

    }

    private IEnumerator SendPostRequest(string command, string postData)
    {
        byte[] pData = System.Text.Encoding.ASCII.GetBytes(postData.ToCharArray());
        Debug.Log("SendPostRequest :" + command + ": " + postData);

        yield return new WaitForEndOfFrame();

        // make api call and yield till return made
        WWW api = new WWW(API_SERVER + command, pData, headers);
        yield return api;
        
        if (string.IsNullOrEmpty(api.error))
            Debug.Log("NetworkManager Success: " + api.text);
        else
            Debug.LogError("NetworkManager Error: " + api.error);
    }

    public void Send_CreateUser(string username = "testuser_00")
    {
        string createUser_string = "{\"username\":\"" + username + "\"}";

        StartCoroutine(SendPostRequest("create_user", createUser_string));
    }
    public void Send_PurchaseSword(string username)
    {
        string data = "{\"username\":\"" + username + "\"}";
        StartCoroutine(SendPostRequest("purchase_a_sword", data));
    }
    public void Send_PurchaseAxe(string username)
    {
        string data = "{\"username\":\"" + username + "\"}";
        StartCoroutine(SendPostRequest("purchase_an_axe", data));
    }
    public void Send_JoinGuild(string username, int guild)
    {
        string data = "{\"username\":\"" + username + "\", \"guild_type\": " + guild + "}";
        StartCoroutine(SendPostRequest("join_guild", data));
    }
    public void Send_PlayerDeath(string username, int guild, int level, string weapon, int earned_gold, int killCount)
    {
        string game_data = "{\"username\":\"" + username + "\""
                                    + ",\"guild_type\": " + guild
                                    + ",\"level\": " + level
                                    + ",\"weapon_type\": \"" + weapon + "\""
                                    + ",\"gold\": " + earned_gold
                                    + ",\"num_kills\": " + killCount
                                    + "}";
        StartCoroutine(SendPostRequest("player_died", game_data));
    }
}
