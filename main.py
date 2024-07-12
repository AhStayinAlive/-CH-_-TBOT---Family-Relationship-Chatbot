import re

from pyswip import Prolog
prolog = Prolog()
prolog.consult("kb.pl")

#for sentence pattern relationship
singular_rel= {
    "brother", "sister", "father", "mother",
    "grandmother", "grandfather", "child", "daughter",
    "son", "uncle", "aunt"
}

plural_rel = {
    "siblings", "parents", "sisters", "brothers", "relatives",
    "daughters", "sons", "children"
}
#for question pattern : would capture the content that follows
questions = {
    r'Are (.+) and (.+) siblings\?',                r'Who are the siblings of (.+)\?',   #1
    r'Is (.+) a sister of (.+)\?',                  r'Who are the sisters of (.+)\?',    #2
    r'Is (.+) a brother of (.+)\?',                 r'Who are the brothers of (.+)\?',   #3
    r'Is (.+) the mother of (.+)\?',                r'Who is the mother of (.+)\?',      #4
    r'Is (.+) the father of (.+)\?',                r'Who is the father of (.+)\?',      #5
    r'Are (.+) and (.+) the parents of (.+)\?',     r'Who are the parents of (.+)\?',    #6
    r'Is (.+) a grandmother of (.+)\?',             r'Is (.+) a grandfather of (.+)\?',    #7
    r'Is (.+) a daughter of (.+)\?',                r'Who are the daughters of (.+)\?',  #8
    r'Is (.+) a son of (.+)\?',                     r'Who are the sons of (.+)\?',       #9
    r'Is (.+) a child of (.+)\?',                   r'Who are the children of (.+)\?',   #10
    r'Are (.+), (.+) and (.+) children of (.+)\?',  r'Is (.+) an aunt of (.+)\?',        #11
    r'Is (.+) an uncle of (.+)\?',                  r'Are (.+) and (.+) relatives\?',    #12
}
#for statements pattern : would capture the content that follows
statements = {
    r'(.+) and (.+) are siblings\.',        r'(.+) is a brother of (.+)\.',                   #1
    r'(.+) is a sister of (.+)\.',          r'(.+) is the father of (.+)\.',                  #2
    r'(.+) is the mother of (.+)\.',        r'(.+) and (.+) are the parents of (.+)\.',       #3
    r'(.+) is a grandmother of (.+)\.',     r'(.+) is a grandfather of (.+)\.',               #4
    r'(.+) is a child of (.+)\.',           r'(.+), (.+) and (.+) are children of (.+)\.',    #5
    r'(.+) is a daughter of (.+)\.',        r'(.+) is a son of (.+)\.',                       #6
    r'(.+) is an uncle of (.+)\.',          r'(.+) is an aunt of (.+)\.'                      #7
}

prolog_q = set()

def get_first_word(input_string):
    words = input_string.split()
    if words:
        return words[0]
    else:
        return None

def statement_processing(input_statement):
    for pattern in statements:
        checkPattern = re.match(pattern, input_statement)

        if checkPattern:
            # print(pattern)
            title = ""
            for rel in plural_rel:
                if re.search(rel, pattern):
                    title = rel
            for rel in singular_rel:
                if re.search(rel, pattern):
                    title = rel


            group_statement = checkPattern.groups()
            # print(f"View Check Pattern : {checkPattern}")
            # print(f"View title {title}")

            # print(f"Group : {group_statement}")

            if any(
                re.match(pattern, input_statement)
                for pattern in (plural_rel | singular_rel | questions | statements)
            ):
                # print(f"{plural_rel | singular_rel | questions | statements}")
                # print(group_statement)
                subjects = [
                    subject[:-1] if subject[-1:] == "," else subject
                    for subject in group_statement if subject != "and"
                ]
                # print(f"View Pair : {subjects}")

                if subjects[0] != subjects[1]:
                    # try:
                        if title == "siblings":
                            #X and Y are siblings
                            prolog_query = f"{title}({subjects[0]}, {subjects[1]})"
                            if prolog_query not in(prolog_q):
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break

                            prolog_query = f"{title}({subjects[1]}, {subjects[0]})"
                            if prolog_query not in (prolog_q):
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"siblingS: {prolog_query}")
                        elif title == "parents":
                            prolog_query = f"{title}({subjects[0]},{subjects[2]})"
                            if prolog_query not in (prolog_q):
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"Asserted: {prolog_query}")

                            prolog_query = f"{title}({subjects[1]},{subjects[2]})"
                            if prolog_query not in (prolog_q):
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"parentS: {prolog_query}")

                        elif title == "father":
                            prolog_query = f"male({subjects[0]})"
                            if prolog_query not in (prolog_q) and f"female({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"Asserted: {prolog_query}")

                            prolog_query = f"father({','.join(subjects)})"
                            if prolog_query not in (prolog_q) and f"female({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"Asserted: {prolog_query}")

                        elif title == "mother":
                            prolog_query = f"female({subjects[0]})"
                            if prolog_query not in (prolog_q) and f"male({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"Asserted: {prolog_query}")

                            prolog_query = f"mother({','.join(subjects)})"
                            if prolog_query not in (prolog_q) and f"male({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"Asserted: {prolog_query}")

                        elif title == "sister":
                            # X is a sister of Y
                            prolog_query = f"female({subjects[0]})"
                            if prolog_query not in (prolog_q) and f"male({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"sister F: {prolog_query}")

                            #X and Y are siblings
                            prolog_query = f"siblings({subjects[0]}, {subjects[1]})"
                            if prolog_query not in (prolog_q) and f"male({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break

                            prolog_query = f"siblings({subjects[1]}, {subjects[0]})"
                            if prolog_query not in (prolog_q) and f"male({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"siblingS: {prolog_query}")

                            prolog_query = f"sister({subjects[0]}, {subjects[1]})"
                            if prolog_query not in (prolog_q) and f"male({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"sister: {prolog_query}")


                        elif title == "brother":
                            prolog_query = f"male({subjects[0]})"
                            if prolog_query not in (prolog_q) and f"female({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"brother M: {prolog_query}")

                            #X and Y are siblings
                            prolog_query = f"siblings({subjects[0]}, {subjects[1]})"
                            if prolog_query not in (prolog_q) and f"female({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break

                            prolog_query = f"siblings({subjects[1]}, {subjects[0]})"
                            if prolog_query not in (prolog_q) and f"female({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"siblingS: {prolog_query}")

                            prolog_query = f"brother({subjects[0]}, {subjects[1]})"
                            if prolog_query not in (prolog_q) and f"female({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"brother: {prolog_query}")


                        elif title == "children" or title == "child":

                            if len(subjects) > 2:

                                print(title)
                                prolog_query = f"parents({subjects[3]},{subjects[0]})"
                                if prolog_query not in (prolog_q):
                                    prolog_q.add(prolog_query)
                                    prolog.assertz(prolog_query)
                                else:
                                    print("Invalid!")
                                    break
                                print(f"Asserted: {prolog_query}")

                                prolog_query = f"parents({subjects[3]},{subjects[1]})"
                                if prolog_query not in (prolog_q):
                                    prolog_q.add(prolog_query)
                                    prolog.assertz(prolog_query)
                                else:
                                    print("Invalid!")
                                    break

                                print(f"Asserted: {prolog_query}")

                                prolog_query = f"parents({subjects[3]},{subjects[2]})"
                                if prolog_query not in (prolog_q):
                                    prolog_q.add(prolog_query)
                                    prolog.assertz(prolog_query)
                                else:
                                    print("Invalid!")
                                    break
                                print(f"Asserted: {prolog_query}")

                            else:
                                print(title)
                                prolog_query = f"parents({subjects[1]},{subjects[0]})"
                                if prolog_query not in (prolog_q):
                                    prolog_q.add(prolog_query)
                                    prolog.assertz(prolog_query)
                                else:
                                    print("Invalid!")
                                    break
                                print(f"Asserted: {prolog_query}")

                        elif title == "aunt":
                            prolog_query = f"female({subjects[0]})"     #aunt
                            if prolog_query not in (prolog_q) and f"male({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break

                            prolog_query = f"aunt({subjects[0]},{subjects[1]})"
                            if prolog_query not in (prolog_q) and f"male({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break

                        elif title == "uncle":
                            prolog_query = f"male({subjects[0]})"
                            if prolog_query not in (prolog_q) and f"female({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break

                            prolog_query = f"uncle({subjects[0]},{subjects[1]})"
                            if prolog_query not in (prolog_q) and f"female({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                        elif title == "son":
                            prolog_query = f"male({subjects[0]})"
                            if prolog_query not in (prolog_q) and f"female({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"Asserted: {prolog_query}")

                            prolog_query = f"parents({subjects[1]},{subjects[0]})"
                            if prolog_query not in (prolog_q) and f"female({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"Asserted: {prolog_query}")

                        elif title == "daughter":
                            prolog_query = f"female({subjects[0]})"
                            if prolog_query not in (prolog_q) and f"male({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"Asserted: {prolog_query}")

                            prolog_query = f"parents({subjects[1]},{subjects[0]})"
                            if prolog_query not in (prolog_q) and f"male({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"Asserted: {prolog_query}")

                        elif title == "grandmother":

                            # print(f"Asserted: {title}")

                            prolog_query = f"female({subjects[0]})"
                            if prolog_query not in (prolog_q) and f"male({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"Asserted: {prolog_query}")

                            prolog_query = f"grandmother({subjects[0]},{subjects[1]})"
                            if prolog_query not in (prolog_q) and f"male({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break

                        elif title == "grandfather":

                            prolog_query = f"male({subjects[0]})"
                            if prolog_query not in (prolog_q) and f"female({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"Asserted: {prolog_query}")

                            prolog_query = f"grandfather({subjects[0]},{subjects[1]})"
                            if prolog_query not in (prolog_q) and f"female({subjects[0]})" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                        else:
                            prolog_query = f"{title}({','.join(subjects)})"
                            if prolog_query not in (prolog_q) and f"female({subjects[0]}" not in prolog_q:
                                prolog_q.add(prolog_query)
                                prolog.assertz(prolog_query)
                            else:
                                print("Invalid!")
                                break
                            # print(f"Asserted: {prolog_query}")

                        answer = list(prolog.query(prolog_query))

                        if answer:
                            print("OK I learned something today.")
                            # print("Query : " + prolog_query)
                        else:
                            print("No Knowledge Asserted.")
                        break  # Exit the loop after a successful match
                    # except Exception as e:
                    #     print("Error, Try Again!")
                else:
                    print("Invalid relation.")

def question_processing(question_input):
    for pattern in questions:
        checkPattern = re.match(pattern, question_input)

        if checkPattern:
            group_question = checkPattern.groups()
            title = ""

            for rel in plural_rel:
                if re.search(rel, pattern):
                    title = rel
                    # print(rel)

            for rel in singular_rel:
                if re.search(r'\b%s' %rel, pattern):
                    title = rel
                    # print(rel)

            if any(
                re.match(pattern, question_input)
                for pattern in (plural_rel | singular_rel | questions | statements)
            ):
                subjects = [
                    subject[:-1] if subject[-1:] == "," else subject
                    for subject in group_question if subject != "and"
                ]
                # print(f"View Pair: {subjects}")

                # sentence = "This is an example sentence."

                # Split the sentence into words
                words = question_input.split()

                # Get the first word
                firstword = words[0]

                if title:
                    try:
                        #it will display yes or no questions that are not asking for names
                        if firstword != "Who":
                            prolog_query = f"{title}({', '.join(subjects)})"
                            # print(f"What query: {prolog_query}")

                            # Querying Prolog
                            answer = list(prolog.query(prolog_query))

                            if answer:
                                print("Yes")
                            else:
                                print("No")

                        else: #will display the questions asking for names

                            if title == "children" or title == "child":
                                prolog_query = f"parents({subjects[0].lower()},X)"
                            elif title == "son":
                                prolog_query = f"parents({subjects[0].lower()},X) , male(X)"
                            elif title == "daughter":
                                prolog_query = f"parents({subjects[0].lower()},X) , female(X)"
                            elif title == "father":
                                prolog_query = f"parents(X,{subjects[0].lower()}) , male(X)"
                            elif title == "mother":
                                prolog_query = f"parents(X,{subjects[0].lower()}) , female(X)"
                            elif title == "brother":
                                prolog_query = f"brother(X,{subjects[0].lower()}) , male(X)"
                            elif title == "sister":
                                prolog_query = f"sister(X,{subjects[0].lower()}) , female(X)"
                            elif title == "siblings":
                                prolog_query = f"siblings(X,{subjects[0].lower()})"
                            else:
                                prolog_query = f"{title}(X,{subjects[0].lower()})"

                            print(f" query: {prolog_query}")

                            # Querying Prolog
                            answer = list(prolog.query(prolog_query))
                            # set to keep track of unique names so it will not prompt redundant names
                            unique = set()

                            for x in answer:
                                name = x['X']
                                # Check if the name is not in the set, then print and add it to the set
                                if name not in unique:
                                    print(f"- {name}")
                                    unique.add(name)

                        # prolog_query = f"{title}(['X'],{subjects[0]})"
                        # print(f"What query: {prolog_query}")
                        # answer = list(prolog.query(prolog_query))
                        # if answer:
                        #     print(f"{answer[0]['X']}")
                        # else:
                        #     print("I don't know")


                        # print(f"What query: {prolog_query}")
                        # print("Answer:", "Yes!" if (answer is not None) else "No!")
                        # print(answer)
                        break  # Exit the loop after a successful match
                    except Exception as e:
                        print("Impossible!")
                else:
                    print("Invalid relation.")


while True:
    print("\n\n=========================\n       CH(^_^)TBOT \n=========================")
    print("1) Statement Prompt")
    print("2) Question Prompt")
    print("3) Exit")
    print("=========================\nInput Choice : ")
    choice = input("> ")
    print("\n=========================")
    if choice == "1":
        print("(^_^) Enter Statement")
        statement = input("> ")
        statement = statement.lower()  # Update the variable with the lowercase value
        statement_processing(statement)
    elif choice == "2":
        print("(0_0)? Enter Question")
        question = input("> ")
        question_processing(question)
    elif choice == "3":
        print("Exiting.... :(")
        break
    else:
        print("Error, please try again.")