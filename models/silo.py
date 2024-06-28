"""Joke silo for each user."""

from . import REDIS
from utils.generate_content import (
    generate_random,
    generate_dynamic,
    generate_text_from_id,
    DotProduct,
)


class Silo:
    """Silo class.

    Methods:
        create_silo(session_id: str) -> None:
        repopulate_silo(session_id: str) -> None:
        include_joke(session_id: str, joke_id: str) -> None:
        exclude_joke(session_id: str, joke_id: str) -> None:
        get_jokes(session_id: str, count: int = 5) -> list:
    """

    __silo = REDIS

    @classmethod
    def create_silo(cls, session_id: str) -> None:
        """Create a new silo from a user's session.

        The joke field is to be populated with the user's preferences present
        in the user's database. If the field is empty, the joke field is
        populated with randomly generated jokes.

        Args:
            session_id: ID generated for the user's session
        """
        # TODO: Include jokes from user's permenent includes to populate silo
        cls.__silo.set(
            session_id, {"jokes": "this is a joke", "includes": {}, "excludes": {}}
        )

    @classmethod
    def destroy_silo(cls, session_id: str) -> None:
        """Destroy a silo from a user's session.

        Args:
            session_id: ID generated for the user's session
        """
        cls.__silo.delete(session_id)

    @classmethod
    def include_joke(cls, session_id: str, joke_id: str) -> None:
        """Include a joke to a user's silo.

        Args:
            session_id: ID generated for the session
            joke_id:    ID of the joke to include
        """
        if cls.__silo.exist(session_id, "excludes", joke_id):
            cls.__silo.remove(session_id, "excludes", joke_id)
        cls.__silo.insert(session_id, "includes", joke_id)
        # cls.__silo.append(session_id, "includes", 140, joke_id)

    @classmethod
    def exclude_joke(cls, session_id: str, joke_id: str) -> None:
        """Exclude a joke from a user's silo.

        Args:
            session_id: ID generated for the session
            joke_id:    ID of the joke to exclude
        """
        if cls.__silo.exist(session_id, "includes", joke_id):
            cls.__silo.remove(session_id, "includes", joke_id)
        cls.__silo.insert(session_id, "excludes", joke_id)
        # cls.__silo.append(session_id, "excludes", 140, joke_id)

    @classmethod
    def get_jokes(cls, session_id: str, count: int = 5) -> list:
        """Get the jokes avaliable for a user from the silo.

        Args:
            session_id: ID generated for the session
            count:      No of results to return
        Returns:
            List of jokes present in user's silo
        Raises:
            KeyError
        """
        jokes = cls.__silo.get(session_id, "jokes")
        if isinstance(jokes, str):
            pass
        elif isinstance(jokes, list):
            if isinstance(jokes[0], list):
                jokes = jokes[0]
        # print("\n\njokes, from get_jokes\n\n", jokes)
        if count == -1:
            return jokes
        return jokes[:count]

    @classmethod
    def repopulate_jokes(cls, session_id: str) -> None:
        """Repopulate a user's joke silo

        Args:
            session_id: ID generated for the user's session
        """
        jokes_in_stream = cls.get_jokes(session_id, -1)
        excludes = cls.__silo.get(session_id, "excludes")
        includes = cls.__silo.get(session_id, "includes")
        print("These are includes", includes, "and excludes", excludes)
        # Use excludes and includes to repopulate jokes.
        jokes_left_over = jokes_in_stream[5:]  # Can change 5: to count:
        amount_left = len(jokes_left_over)
        amount_needed_to_bulk_up = 20 - amount_left

        # Use the given id to get personalized jokeIds
        # if len(list(includes)) == 0:
        if includes[0] == {}:
            joke_ids = generate_random(amount_needed_to_bulk_up - 2)
        else:
            joke_ids = generate_dynamic(
                [list(obj.keys())[0] for obj in includes], amount_needed_to_bulk_up - 2
            )
        print("The joke_ids genrated are", joke_ids)
        # Exclude the exclude_ids from the jokeIds generated.
        if excludes[0] != {}:
            for id in [list(obj.keys())[0] for obj in excludes]:
                joke_ids.remove(id)
        jokes_left_over.extend(generate_text_from_id(joke_ids))
        amount_needed_to_bulk_up = 20 - len(jokes_left_over)
        addendum = generate_text_from_id(generate_random(amount_needed_to_bulk_up))
        jokes_left_over.extend(addendum)

        cls.__silo.set(
            session_id,
            {"jokes": jokes_left_over, "includes": {}, "excludes": {}},
        )
        # TODO: update silo's jokes with newly generated content.
