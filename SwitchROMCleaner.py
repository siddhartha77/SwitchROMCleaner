import os
import re

def main():
    bytes = 0
    
    for subdir, dirs, files in os.walk(os.getcwd()):
        titles = {}
            
        for file in files:
        
            if file.endswith(".nsp") or file.endswith(".nsz") or file.endswith(".xci") or file.endswith(".xcz"):
                titleId = ""
                version = -1
                searchResult = re.search(r'\[(0100[0-9A-Fa-f]{12})\]\[v?(\d+)\]', file)            
                
                if searchResult:
                    titleId = searchResult.group(1).upper()
                    version = int(searchResult.group(2))
                    
                if (titleId != "") and (version > -1) and (version % 65536) == 0:
                    if titleId in titles:
                        if version > titles[titleId]["version"]:
                            bytes += os.path.getsize(os.path.join(subdir, titles[titleId]["file"]))
                            os.remove(os.path.join(subdir, titles[titleId]["file"]))
                            print("Deleted " + os.path.join(subdir, titles[titleId]["file"]))
                            titles[titleId]["version"] = version
                            titles[titleId]["file"] = file
                        elif version < titles[titleId]["version"]:
                            bytes += os.path.getsize(os.path.join(subdir, file))
                            os.remove(os.path.join(subdir, file))
                            print("Deleted " + os.path.join(subdir, file))
                    else:
                        titles[titleId] = {}
                        titles[titleId]["version"] = version
                        titles[titleId]["file"] = file

    print(f"Saved {(bytes / 1000000):,.0f} MB")

if __name__ == '__main__':
    main()