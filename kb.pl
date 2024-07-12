% KB

:- dynamic male/1.
:- dynamic female/1.

:- dynamic siblings/2.
:- dynamic brother/2.
:- dynamic sister/2.
:- dynamic child/2.

:- dynamic parents/2.
:- dynamic father/2.
:- dynamic mother/2.
:- dynamic daughter/2.
:- dynamic son/2.

:- dynamic grandparent/2.
:- dynamic grandmother/2.

:- dynamic relative/2.
:- dynamic uncle/2.
:- dynamic aunt/2.

% Rules for querying relationships
siblings(X,Y) :-
    parents(Z,Y),
    parents(Z,X),
    dif(X,Y).

% Define grandparent relationships
grandparent(X, Y) :-
    parents(X, Z),
    parents(Z, Y).

brother(X,Y) :-
    male(X),
    siblings(X,Y).

sister(X,Y) :-
    female(X),
    siblings(X,Y).

father(X, Y) :-
    dif(X,Y),
    male(X),
    parents(X, Y).

mother(X, Y) :-
    dif(X,Y),
    female(X),
    parents(X, Y).

son(X,Y) :-
    male(X),
    parents(Y,X).

daughter(X,Y) :-
    female(X),
    parents(Y,X).

grandfather(X,Y) :-
    dif(X,Y),
    male(X),
    grandparent(X,Y).

grandmother(X,Y) :-
    dif(X,Y),
    female(X),
    grandparent(X,Y).

uncle(X,Y) :-
    male(X),
    siblings(X,Z),
    parents(Z,Y).

aunt(X,Y) :-
    female(X),
    siblings(X,Z),
    parents(Z,Y).

relatives(X,Y) :-
    siblings(X,Y);
    parents(X,Y);
    parents(Y,X);
    grandparent(X,Y);
    grandparent(Y,X);
    uncle(X,Y);
    uncle(Y,X);
    aunt(X,Y);
    aunt(Y,X).

children(X, Y) :-
    parents(Y, X).

child(X, Y) :-
    parents(Y, X).


