from pprint import pprint
import pymel.core as pm

def main():
    unknown_plugins = pm.unknownPlugin(query=True, list=True) or list()

    for plugin in unknown_plugins:
        pm.unknownPlugin(plugin, remove=True)

    print "The following unknown plugins removed!"
    pprint(unknown_plugins)
    print 

if __name__ == "__main__":
    main()