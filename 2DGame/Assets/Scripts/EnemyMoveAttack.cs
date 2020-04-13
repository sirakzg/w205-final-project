using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyMoveAttack : MonoBehaviour
{
    private Creatures_Character_Controller controller;
    private bool attacking = false;
    private int health = 2;

    // Start is called before the first frame update
    void Start()
    {
        controller = this.gameObject.GetComponent<Creatures_Character_Controller>();
    }

    // Update is called once per frame
    void Update()
    {
        // the dead dont move
        if (health < 0) return;

        // one state, walk towards player
        float delta = CharacterManager.Distance2Player(this.transform.position);

        if (Mathf.Abs(delta) < .67f)
        {
            if (!attacking )
                StartCoroutine(AttackPlayer());
        }
        else
            controller.PlayAttack(false);


        if (delta - 0.1f > 0)
            controller.PlayMove(1f);
        else if (delta + 0.1f < 0)
            controller.PlayMove(-1f);
        else
            controller.PlayMove(0f);

    }

    IEnumerator AttackPlayer()
    {
        attacking = true;
        controller.PlayAttack(true);
        CharacterManager.EnemeyAttacking(this.transform.position);

        // stop looping animation
        yield return new WaitForSeconds(0.25f);
        controller.PlayAttack(false);

        // delay till next attack allowed
        yield return new WaitForSeconds(1.75f);
        attacking = false;
    }


    private void PlayerAttacks(float player_x)
    {
        if (Mathf.Abs(player_x - this.transform.position.x) < 0.7)
        {
            //Debug.Log("Player Hits Enemy!");
            health--;
        }

        if (health == 0)
        {
            controller.KilledByPlayer();
            GameManager.PlayerKilledEnemy();
        }

    }
}
