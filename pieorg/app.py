import sqlite3
from sqlite3 import Error
import click
from art import text2art


def connectToDb(dbname):
    try:
        conn = sqlite3.connect(dbname)
        return conn
    except Error:
        print(Error)


def getNewTableIfNotExistsQuery(fandomname):
    query = """CREATE TABLE IF NOT EXISTS %s_table 
            (id INTEGER PRIMARY KEY, fandom text NOT NULL, 
            title text NOT NULL, author text NOT NULL, 
            link text NOT NULL, categ text NOT NULL,
            desc text, 
            genre1 text NOT NULL, genre2 text NOT NULL, 
            typefic text NOT NULL, lovemeter integer NOT NULL,
            comp text NOT NULL)
            """ % fandomname
    return query


#the table in each fandom db is denoted as <fandom>_table
#get list of categories/folders
def getListOfCatsinFandomQuery(fandom):
    query = """SELECT distinct categ from %s_table """ % (fandom)
    return query


@click.command()
@click.option('--fandom', prompt='Enter the fandom name=>')
@click.option('--title', prompt='Enter the title of the fic=>')
@click.option('--author', prompt='Enter the author name=>')
@click.option('--link', prompt='Enter the link of the fic=>')
@click.option('--categ',
              prompt='Enter the category or folder name for the fic=>')
@click.option('--desc',
              prompt='Enter the description of the fic(optional)=>',
              default='nothing')
@click.option('--genre1', prompt='Enter the first genre=>')
@click.option('--genre2', prompt='Enter the second genre=>')
@click.option('--typefic',
              prompt='Enter the type of fic(novel or one-shot)=>',
              type=click.Choice(['novel', 'os'], case_sensitive=True))
@click.option('--lovemeter',
              prompt='Enter the love meter(1 - 5, 5 being the highest)=>',
              type=click.Choice(['1', '2', '3', '4', '5']))
@click.option('--comp',
              prompt='Is the story complete (y or n)=>',
              type=click.Choice(['y', 'n'], case_sensitive=False))
def insertFic(fandom, title, author, link, categ, desc, genre1, genre2,
              typefic, lovemeter, comp):
    conn = connectToDb(fandom)  #each fandom will have a separate dababase
    cursorObj = conn.cursor()  #get the cursor object for fandom db

    tableQuery = getNewTableIfNotExistsQuery(fandom)
    cursorObj.execute(tableQuery)
    conn.commit()

    #get and display folder names (which are also the column 'categ' in the fandom table)
    click.echo('You now have the categories/folders:')
    fQuery = getListOfCatsinFandomQuery(fandom)
    cursorObj.execute(fQuery)
    rowsOfFolderNames = cursorObj.fetchall()

    for row in rowsOfFolderNames:
        click.echo(row)

    title = title.replace(' ', '_')
    author = author.replace(' ', '_')
    desc = desc.replace(' ', '_')

    entities = (fandom, title, author, link, categ, desc, genre1, genre2,
                typefic, lovemeter, comp)
    cursorObj.execute(
        '''INSERT INTO %s_table(fandom, title, 
        author, link, categ, desc, genre1, 
        genre2, typefic, lovemeter, comp)
        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''' % fandom, entities)
    conn.commit()

    cursorObj.close()
    conn.close()

    click.echo('Fic inserted!')


def getAllFicsInFandomQuery(fandom):
    query = """SELECT * FROM %s_table""" % fandom
    return query


def getAllFicsWithGenreQuery(fandom, genre):
    query = """SELECT * from %s_table where genre1='%s' or genre2='%s'""" % (
        fandom, genre, genre)
    return query


def getAllFicsWithTypeQuery(fandom, typefic):
    query = """SELECT * from %s_table where typefic='%s'""" % (fandom, typefic)
    return query


def getAllFicsWithMinLovemeterQuery(fandom, lovemeter):
    query = """SELECT * from %s_table where lovemeter>%d""" % (fandom,
                                                               int(lovemeter))
    return query


def getAllFicsWithAuthorQuery(fandom, author):
    # query = """SELECT * from %s_table where author = %s""" % (fandom, author)
    query = "SELECT * from " + fandom + "_table where author = '" + author + "'"
    return query


def getAllFicsWithCategoryQuery(fandom, categ):
    query = """SELECT * from %s_table where categ='%s'""" % (fandom, categ)
    return query


def getAllCategoriesQuery(fandom):
    query = """SELECT DISTINCT categ from %s_table""" % fandom
    return query


def getAllFicsByGenreAndLovemeter(fandom, genre, lovemeter):
    query = """SELECT * from %s_table where (genre1='%s' OR genre2='%s') and (lovemeter>%d)""" % (
        fandom, genre, genre, int(lovemeter))
    return query


def getAllFicsByDescQuery(fandom, desc):
    query = "SELECT * from " + fandom + "_table " + "where desc LIKE " + "'%" + desc + "%'"
    return query


def getOnlyCompletedFicsInFandomQuery(fandom):
    query = """SELECT * FROM %s_table where comp='y'""" % fandom
    return query


def displaySearchResults(fQuery, fandom):
    conn = connectToDb(fandom)
    cursorObj = conn.cursor()
    cursorObj.execute(fQuery)
    rows = cursorObj.fetchall()

    for row in rows:
        click.echo(row)

    cursorObj.close()
    conn.close()


@click.command()
@click.option('--fandom', prompt='Enter the fandom=>')
def displayAllFicsInFandom(fandom):
    fQuery = getAllFicsInFandomQuery(fandom)
    displaySearchResults(fQuery, fandom)


@click.command()
@click.option('--fandom', prompt='Enter the fandom=>')
def displayOnlyCompletedFics(fandom):
    fQuery = getOnlyCompletedFicsInFandomQuery(fandom)
    displaySearchResults(fQuery, fandom)


@click.command()
@click.option('--fandom', prompt='Enter the fandom=>')
@click.option('--genre', prompt='Enter the genre to search=>')
def displayFicsWithGenre(fandom, genre):
    fQuery = getAllFicsWithGenreQuery(fandom, genre)
    displaySearchResults(fQuery, fandom)


@click.command()
@click.option('--fandom', prompt='Enter the fandom=>')
@click.option('--typefic',
              prompt='Enter the type of fic to search(novel or os)=>')
def displayFicsAccToType(fandom, typefic):
    fQuery = getAllFicsWithTypeQuery(fandom, typefic)
    displaySearchResults(fQuery, fandom)


@click.command()
@click.option('--fandom', prompt='Enter the fandom=>')
@click.option(
    '--lovemeter',
    prompt='Enter the minimum love meter of fics to search for(1 to 5)=>')
def displayFicsAccToMinLovemeter(fandom, lovemeter):
    fQuery = getAllFicsWithMinLovemeterQuery(fandom, lovemeter)
    displaySearchResults(fQuery, fandom)


@click.command()
@click.option('--fandom', prompt='Enter the fandom=>')
@click.option('--author', prompt='Enter the author name=>')
def displayFicsAccToAuthor(fandom, author):
    fQuery = getAllFicsWithAuthorQuery(fandom, author)
    displaySearchResults(fQuery, fandom)


@click.command()
@click.option('--fandom', prompt='Enter the fandom=>')
@click.option('--categ', prompt='Enter the category/folder name=>')
def displayFicsAccToCateg(fandom, categ):
    fQuery = getAllFicsWithCategoryQuery(fandom, categ)
    displaySearchResults(fQuery, fandom)


@click.command()
@click.option('--fandom', prompt='Enter the fandom=>')
def displayAllCateg(fandom):
    fQuery = getAllCategoriesQuery(fandom)
    displaySearchResults(fQuery, fandom)


@click.command()
@click.option('--fandom', prompt='Enter the fandom=>')
@click.option('--genre', prompt='Enter the genre=>')
@click.option('--lovemeter', prompt='Enter the min lovemeter=>')
def displayFicsAccToGenreAndLovemeter(fandom, genre, lovemeter):
    fQuery = getAllFicsByGenreAndLovemeter(fandom, genre, lovemeter)
    displaySearchResults(fQuery, fandom)


@click.command()
@click.option('--fandom', prompt='Enter the fandom=>')
@click.option('--desc', prompt='Enter the description=>')
def displayFicsAccToDesc(fandom, desc):
    fQuery = getAllFicsByDescQuery(fandom, desc)
    displaySearchResults(fQuery, fandom)


def displayOptions():
    click.echo('Choose an option from the list:')
    click.echo('Type 1 to Display all fics')
    click.echo('Type 2 to Display all completed fics')
    click.echo('Type 3 to Display all fics for a particular category/folder')
    click.echo('Type 4 to Display all fics for a particular author')
    click.echo('Type 5 to Display all fics for a particular genre')
    click.echo('Type 6 to Display all fic categories you have created')
    click.echo('Type 7 to Display all fics with a minimum lovemeter')
    click.echo('Type 8 to Display all fics of the type(novel or os)')
    click.echo('Type 9 to Display all fics of a genre and min lovemeter')
    click.echo('Type 10 to Display all fics with a description')

    choice = click.prompt('Type your choice=>')
    if choice == '1':
        displayAllFicsInFandom()
    elif choice == '2':
        displayOnlyCompletedFics()
    elif choice == '3':
        displayFicsAccToCateg()
    elif choice == '4':
        displayFicsAccToAuthor()
    elif choice == '5':
        displayFicsWithGenre()
    elif choice == '6':
        displayAllCateg()
    elif choice == '7':
        displayFicsAccToMinLovemeter()
    elif choice == '8':
        displayFicsAccToType()
    elif choice == '9':
        displayFicsAccToGenreAndLovemeter()
    elif choice == '10':
        displayFicsAccToDesc()
    else:
        click.echo('Incorrect choice, please try again!')
    return


def editStoryDesc(fandom, id, desc):
    query = """UPDATE %s_table set desc='%s' where id = %d """ % (fandom, desc,
                                                                  int(id))
    conn = connectToDb(fandom)
    cursorObj = conn.cursor()
    cursorObj.execute(query)
    conn.commit()


def editStoryStatus(fandom, id, yes):
    query = """UPDATE %s_table set comp='%s' where id = %d """ % (fandom, yes,
                                                                  int(id))
    conn = connectToDb(fandom)
    cursorObj = conn.cursor()
    cursorObj.execute(query)
    conn.commit()


@click.command()
@click.option(
    '--a',
    prompt='Enter d to edit description or s to edit status of the story=>',
    type=click.Choice(['d', 's'], case_sensitive=True))
def editOptions(a):
    fandom = click.prompt('Enter the fandom=>')
    fQuery = getAllFicsInFandomQuery(fandom)
    displaySearchResults(fQuery, fandom)
    choice = click.prompt('Select a story by its id number=>')
    if a == 'd':
        desc = click.prompt('Enter new description=>')
        editStoryDesc(fandom, choice, desc)
    elif a == 's':
        yes = click.prompt('Change status to complete=>(y or n)')
        editStoryStatus(fandom, choice, yes)


def main():
    Art = text2art("PieOrg", font='block', chr_ignore=False)
    click.echo(Art)
    click.echo('Welcome to PieOrg, your story organiser!\n\n')


def showInsertOption():
    insertFic()


def showEditOption():
    editOptions()


def showDisplayOption():
    displayOptions()


@click.command()
@click.option(
    '--a',
    prompt='i for insert option, e for edit and d for display options=>',
    type=click.Choice(['i', 'e', 'd'], case_sensitive=False))
def begin(a):
    main()
    if a == 'i' or a == 'I':
        showInsertOption()
    elif a == 'e' or a == 'E':
        showEditOption()
    elif a == 'd' or a == 'D':
        showDisplayOption()
