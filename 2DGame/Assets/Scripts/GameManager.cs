using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    public static GameManager _instance;
    private string username = "testuser_";

    private int gold = 0;
    private int gameKills = 0;

    //0=sword, 1=axe
    public int weaponType = 0;
    public int guild = 0;

    private bool levelLoaded = false;

    public GameObject menu_UI;
    public GameObject game_UI;
    public Text health_text;
    public Text gold_text;
    public Text kills_text;

    public GameObject instruct_text;
    public GameObject credits_text;

    public GameObject[] weapon_selections;
    public GameObject[] guild_selections;

    private ColorBlock notSelected = new ColorBlock();
    private ColorBlock isSelected = new ColorBlock();

    void Awake()
    {
        // enforce one instance of class per scene
        if (_instance == null)
            _instance = this;
        else return;


        int currentMilliSec = System.DateTime.Now.Millisecond % 1000;
        username += currentMilliSec;

        Color default_color = new Color(0.8784f, 0.8784f, 0.8784f,1f);
        notSelected.colorMultiplier = 1f;
        notSelected.normalColor = default_color;
        notSelected.selectedColor = default_color;
        notSelected.highlightedColor = default_color;
        notSelected.pressedColor = default_color;
        notSelected.disabledColor = new Color(0.8784f, 0.8784f, 0.8784f, 0.50f);

        isSelected.colorMultiplier = 1f;
        isSelected.normalColor = new Color(1f, .77f, 0f, 1f);
        isSelected.selectedColor = new Color(1f, .77f, 0f, 1f);
        isSelected.highlightedColor = default_color;
        isSelected.pressedColor = default_color;
        isSelected.disabledColor = new Color(0.8784f, 0.8784f, 0.8784f, 0.50f);

        guild_selections[guild].GetComponent<Button>().colors = isSelected;
        weapon_selections[weaponType].GetComponent<Button>().colors = isSelected;
    }

    // Start is called before the first frame update
    void Start()
    {
        NetworkManager._instance.Send_CreateUser(username);

    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void StartLevel()
    {
        if (levelLoaded) return;

        levelLoaded = true;
        gameKills = 0;
        kills_text.text = "Kills:\n" + gameKills;

        SceneManager.LoadScene("Scenes/Level1", LoadSceneMode.Additive);
        menu_UI.SetActive(false);
        game_UI.SetActive(true);
        instruct_text.SetActive(true);
        credits_text.SetActive(false);
    }

    public void CloseLevel()
    {
        if (!levelLoaded) return;

        SceneManager.UnloadScene("Scenes/Level1");
        levelLoaded = false;
        menu_UI.SetActive(true);
        game_UI.SetActive(false);

        string weapon = this.weaponType == 0 ? "sword" : "axe";
        NetworkManager._instance.Send_PlayerDeath(username, this.guild, 1, weapon, this.gold, this.gameKills);

    }

    public void PlayerDied()
    {
        StartCoroutine(WaitToLoadMenu());
    }

    IEnumerator WaitToLoadMenu()
    {
        yield return new WaitForSeconds(4);
        CloseLevel();
    }

    public static void PlayerHealthStatus(int player_health)
    {
        if (player_health >= 0)
            _instance.health_text.text = "Health:\n" + player_health;

        if (player_health == -1)
            _instance.PlayerDied();
    }

    public static void PlayerKilledEnemy()
    {
        _instance.gameKills++;
        _instance.gold += 10;
        _instance.kills_text.text = "Kills:\n" + _instance.gameKills;
        _instance.gold_text.text = "Gold:\n" + _instance.gold;
    }

    public void ToggleCredits()
    {
        instruct_text.SetActive(!instruct_text.activeInHierarchy);
        credits_text.SetActive(!credits_text.activeInHierarchy);
    }

    public void SelectWeapon(int weapon)
    {
        if (weapon == this.weaponType) return;

        GameObject selection = weapon_selections[weapon];
        int price = 0;

        if(int.TryParse(selection.GetComponentInChildren<Text>().text,  out price))
        {
            if (gold >= price)
            {
                gold -= price;
                _instance.gold_text.text = "Gold:\n" + _instance.gold;
                selection.GetComponentInChildren<Text>().text = "FREE";
            }
            else return;
        }

        weaponType = weapon;
        
        // needed to send events on selection, regardless of purchase price since swords are free
        if(weaponType == 0)
            NetworkManager._instance.Send_PurchaseSword(username);
        else
            NetworkManager._instance.Send_PurchaseAxe(username);

        // update weapon colors so just selection is highlighted
        ClearSelections(weapon_selections);
        selection.GetComponent<Button>().colors = isSelected;
    }
    public void SelectGuild(int guild)
    {
        if (guild == this.guild) return;

        GameObject selection = guild_selections[guild];
        int price = 0;

        if (int.TryParse(selection.GetComponentInChildren<Text>().text, out price))
        {
            if (gold >= price)
            {
                gold -= price;
                _instance.gold_text.text = "Gold:\n" + _instance.gold;
                selection.GetComponentInChildren<Text>().text = "FREE";
            }
            else return;
        }

        this.guild = guild;
        NetworkManager._instance.Send_JoinGuild(username, this.guild);

        // update guild colors so just selection is highlighted
        ClearSelections(guild_selections);
        selection.GetComponent<Button>().colors = isSelected;
    }

    private void ClearSelections(GameObject[] selectors)
    {
        foreach (GameObject g in selectors)
        {
            g.GetComponent<Button>().colors = notSelected;
        }

    }
}
