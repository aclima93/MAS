
state 0
props L.div M1I M2I P*3 RAI
trans a/1

state 1
props L.div IC M1I M2I P*2 RAI
trans a/2 a1pu/3

state 2
props L.div IC*2 M1I M2I P RAI
trans a/4 a1pu/5

state 3
props L.div M1I M2I P*2 a1
trans a/5 a1do/6

state 4
props L.div IC*3 M1I M2I RAI
trans a1pu/7

state 5
props L.div IC M1I M2I P a1
trans a/7 a1do/8

state 6
props L.div M1B M2I P*2 RAI
trans a/8 d1pu/9

state 7
props L.div IC*2 M1I M2I a1
trans a1do/10

state 8
props L.div IC M1B M2I P RAI
trans a/10 a2pu/11 d1pu/12

state 9
props L.div M2I P*2 d1
trans a/12 d1do/13

state 10
props L.div IC*2 M1B M2I RAI
trans a2pu/14 d1pu/15

state 11
props L.div M1B M2I P a2
trans a/14 a2do/16

state 12
props L.div IC M2I P d1
trans a/15 d1do/17

state 13
props L.div AC M1I M2I P*2 RAI
trans a/17

state 14
props L.div IC M1B M2I a2
trans a2do/18

state 15
props L.div IC*2 M2I d1
trans d1do/19

state 16
props L.div M1B M2B P RAI
trans a/18 d1pu/20 d2pu/21

state 17
props L.div AC IC M1I M2I P RAI
trans a/19 a1pu/22

state 18
props L.div IC M1B M2B RAI
trans d1pu/23 d2pu/24

state 19
props L.div AC IC*2 M1I M2I RAI
trans a1pu/25

state 20
props L.div M2B P d1
trans a/23 d1do/26

state 21
props L.div M1B P d2
trans a/24 d2do/27

state 22
props L.div AC M1I M2I P a1
trans a/25 a1do/27

state 23
props L.div IC M2B d1
trans d1do/28

state 24
props L.div IC M1B d2
trans d2do/29

state 25
props L.div AC IC M1I M2I a1
trans a1do/29

state 26
props L.div AC M1I M2B P RAI
trans a/28 d2pu/30

state 27
props L.div AC M1B M2I P RAI
trans a/29 d1pu/31

state 28
props L.div AC IC M1I M2B RAI
trans d2pu/32

state 29
props L.div AC IC M1B M2I RAI
trans a2pu/33 d1pu/34

state 30
props L.div AC M1I P d2
trans a/32 d2do/35

state 31
props L.div AC M2I P d1
trans a/34 d1do/35

state 32
props L.div AC IC M1I d2
trans d2do/36

state 33
props L.div AC M1B M2I a2
trans a2do/37

state 34
props L.div AC IC M2I d1
trans d1do/36

state 35
props L.div AC*2 M1I M2I P RAI
trans a/36 rpu/38

state 36
props L.div AC*2 IC M1I M2I RAI
trans a1pu/39 rpu/40

state 37
props L.div AC M1B M2B RAI
trans d1pu/41 d2pu/42

state 38
props L.div M1I M2I P r
trans rdo/0 a/40

state 39
props L.div AC*2 M1I M2I a1
trans a1do/43

state 40
props L.div IC M1I M2I r
trans rdo/1

state 41
props L.div AC M2B d1
trans d1do/44

state 42
props L.div AC M1B d2
trans d2do/43

state 43
props L.div AC*2 M1B M2I RAI
trans d1pu/45 rpu/46

state 44
props L.div AC*2 M1I M2B RAI
trans d2pu/47 rpu/48

state 45
props L.div AC*2 M2I d1
trans d1do/49

state 46
props L.div M1B M2I r
trans rdo/6

state 47
props L.div AC*2 M1I d2
trans d2do/49

state 48
props L.div M1I M2B r
trans rdo/50

state 49
props L.div AC*3 M1I M2I RAI
trans rpu/51

state 50
props L.div M1I M2B P*2 RAI
trans a/52 d2pu/53

state 51
props L.div AC M1I M2I r
trans rdo/13

state 52
props L.div IC M1I M2B P RAI
trans a/54 d2pu/55

state 53
props L.div M1I P*2 d2
trans d2do/13 a/55

state 54
props L.div IC*2 M1I M2B RAI
trans d2pu/56

state 55
props L.div IC M1I P d2
trans d2do/17 a/56

state 56
props L.div IC*2 M1I d2
trans d2do/19



