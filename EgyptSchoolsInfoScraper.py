import requests
from bs4 import BeautifulSoup
from FinalSchoolsUrls import urls



headers ={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136'
}

#Links_Page = requests.get('https://egyptschools.info/school/nordic-school-in-cairo/',headers=headers)
#Page_src = Links_Page.content
#Soup = BeautifulSoup(Page_src, "lxml")

def Name_PhotoGetter(soap):
    School_Name = None
    try:
        NameAndPhoto_DIV = soap.find("div", {'class': 'profile-name no-tagline no-rating'})
        if(NameAndPhoto_DIV == None):
            NameAndPhoto_DIV = soap.find("div", {'class': 'profile-name no-tagline has-rating'})
        try:
            Photo = NameAndPhoto_DIV.find('a').attrs['href']
        except:
            Photo = None
        try:
            School_NameArr = NameAndPhoto_DIV.find('h1').text.strip().split(' - ')
            if(len(School_NameArr) == 1):
                School_Name = School_NameArr[0]
            elif(len(School_NameArr) == 2):
                School_Name = School_NameArr[1]
            elif (len(School_NameArr) == 3):
                School_Name = School_NameArr[1]
        except:
            School_Name = None
    except:

        Photo = None
        School_Name = None

    return School_Name,Photo



def AddressAndMapGetter(soap):
    try:
        Address_DIV = soap.find('div', {'class': 'element map-block'})
        try:
            School_Address = Address_DIV.find('div', {'class': 'map-block-address'}).find('p').text
        except:
            School_Address = None
        try:
            SchoolMapDiv = Address_DIV.find('div', {'class': 'location-address'})
            SchoolMap = SchoolMapDiv.find('a').attrs['href']
        except:
            SchoolMap = None

    except:
        School_Address = None
        SchoolMap = None
    return School_Address,SchoolMap



def SchoolContactGetter(Soap):
    try:
        School_Contact_DIV = Soap.find('div', {'class': 'col-md-12 block-type-details'})
        Schools_Contact = School_Contact_DIV.find('p').find('a').text
    except:
        Schools_Contact = None
    return Schools_Contact




def SchoolTypesGetter(Soap):
    try:
        School_Types_DIV = Soap.find('div', {'class': 'col-md-12 block-type-terms'})
        School_Types_Li = School_Types_DIV.find_all('li')
        School_Types = []
        for typee in School_Types_Li:
            School_Types.append(typee.find('span').text)
    except:
        School_Types = None
    return School_Types



def FeesPerClassroom(Soap):
    try:
        SchoolFeesPerGradeDiv = Soap.find('div', {'class': 'col-md-12 block-type-restaurant_menu block-field-rep-feilds'})
        SchoolFeesPerGrade = SchoolFeesPerGradeDiv.find_all("div", {'class': 'single-menu-item mt-30 element'})
        schoolLevel_Fee = {}
        for grade in SchoolFeesPerGrade:
            level = grade.find('span').text
            fee = grade.find('div', {'class': 'menu-price-btn'}).text
            schoolLevel_Fee[level] = fee
    except:
        schoolLevel_Fee = None
    return schoolLevel_Fee



def SchoolPhotosGetter(Soap):
    try:
        SchoolPhotosDIV = Soap.find('div', {'class': 'gallery-grid photoswipe-gallery'})
        Photos = []
        SchoolPhotosLi = SchoolPhotosDIV.find_all('a')
        for p in SchoolPhotosLi:
            Photo = p.attrs['href']
            Photos.append(Photo)
    except:
        Photos = None
    return Photos

def WebsiteGetter(Soap):
    try:
        WebDIV = Soap.find('div', {'class': 'col-md-12 block-type-social_networks'})
        Website = WebDIV.find('li').find('a').attrs['href']
    except:
        Website = None
    return Website


def main(pageLink):
    Links_Page = requests.get(pageLink, headers=headers)
    Page_src = Links_Page.content
    soap = BeautifulSoup(Page_src, "lxml")
    SchoolName,SchoolPhoto = Name_PhotoGetter(soap)
    SchoolAddress,SchoolMap = AddressAndMapGetter(soap)
    SchoolContact = SchoolContactGetter(soap)
    SchoolTypes = SchoolTypesGetter(soap)
    SchoolFees = FeesPerClassroom(soap)
    SchoolPhotos = SchoolPhotosGetter(soap)
    SchoolWebsite = WebsiteGetter(soap)

    print(f'School Name: {SchoolName} ,\nSchool Photo: {SchoolPhoto}\n'
          f'School Address: {SchoolAddress}\nSchool Maps {SchoolMap}\n'
          f'School Tel: {SchoolContact} \nSchool Types: {SchoolTypes}\n'
          f'School Fees: {SchoolFees} \nSchool Photos {SchoolPhotos}\n'
          f'School Website: {SchoolWebsite}\n\n')


for page in urls:
    main(page)





