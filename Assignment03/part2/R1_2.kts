
state 0
props L.div M1I M2I P*2 RAI
trans a/1

state 1
props L.div IC M1I M2I P RAI
trans a/2 a1pu/3

state 2
props L.div IC*2 M1I M2I RAI
trans a1pu/4

state 3
props L.div M1I M2I P a1
trans a/4 a1do/5

state 4
props L.div IC M1I M2I a1
trans a1do/6

state 5
props L.div M1B M2I P RAI
trans a/6 d1pu/7

state 6
props L.div IC M1B M2I RAI
trans a2pu/8 d1pu/9

state 7
props L.div M2I P d1
trans a/9 d1do/10

state 8
props L.div M1B M2I a2
trans a2do/11

state 9
props L.div IC M2I d1
trans d1do/12

state 10
props L.div AC M1I M2I P RAI
trans a/12

state 11
props L.div M1B M2B RAI
trans d1pu/13 d2pu/14

state 12
props L.div AC IC M1I M2I RAI
trans a1pu/15

state 13
props L.div M2B d1
trans d1do/16

state 14
props L.div M1B d2
trans d2do/17

state 15
props L.div AC M1I M2I a1
trans a1do/17

state 16
props L.div AC M1I M2B RAI
trans d2pu/18

state 17
props L.div AC M1B M2I RAI
trans d1pu/19

state 18
props L.div AC M1I d2
trans d2do/20

state 19
props L.div AC M2I d1
trans d1do/20

state 20
props L.div AC*2 M1I M2I RAI
trans rpu/21

state 21
props L.div M1I M2I r
trans rdo/0



