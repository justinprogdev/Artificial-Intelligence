
% Julian has no accidents, no tickets, and a good credit score.
% Bubbles has no accidents, no tickets, and a good credit score.
% Ricky has had an accident, unknown ticket status, and a bad credit score.
% Trever has had an accident, has tickets, and a good credit score.

% Each quote has 1 - 2 Drivers
% Each Driver has a unique set of risk data
	% Accident history (has accidents)
	% Violation History (has tickets)
	% Credit History (has good credit)

% 2 Drivers receive a High Quote Amount if EITHER driver is NOT low risk

% A Driver IS low risk if:
	% They do not have an accident
	% AND They have good credit
	% AND They do NOT have tickets
	% AND They do NOT have Infered Tickets
	


% Predicate checks name to see if it has accidents
has_accident(Driver) :-
    quotes(QUOTES),
	member(quote(Driver, accident, _, _), QUOTES).

% Predicate checks if good credit
has_good_credit(Driver) :-
    quotes(QUOTES),
	member(quote(Driver, _, _, goodCredit), QUOTES).

% Predicate checks if the person has tickets
has_tickets(Driver) :-
    quotes(QUOTES),
	member(quote(Driver, _, tickets, _), QUOTES).

% Predicate Infers a driver has tickets based on known criteria,
% also uses disjunction (connective OR)
infers_has_tickets(Driver):-
    \+has_good_credit(Driver) ; has_accident(Driver).

% Checks risk level
low_risk(Driver) :-
    %if all factors are true, driver has low risk
    % I use connective OR for this as well as connective not
    % I also use inference for tickes if has_tickets info is not available
    \+has_accident(Driver), has_good_credit(Driver),\+has_tickets(Driver), \+infers_has_tickets(Driver).

high_quote_amount(Driver1,Driver2):-
    % if either driver is not low risk, we return true for high quote
    % I use connective OR for this
    \+low_risk(Driver1) ; \+low_risk(Driver2).
    
% There exists a quote for each driver with name, accident history, ticket history, credit score
quotes(QUOTES) :-
    length(QUOTES, 5),
    member(quote(julian, noAccident, noTickets, goodCredit), QUOTES),
    member(quote(bubbles, noAccident, noTickets, goodCredit), QUOTES),
    member(quote(ricky, accident, _, badCredit), QUOTES),
    member(quote(trever, accident, tickets, goodCredit), QUOTES),
	member(quote(noah, accident, _, goodCredit), QUOTES).

