'''
    common XBMC Module
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import cgi
import re
import os
try:
    import cPickle as pickle
except:
    import pickle
import base64
import unicodedata
import urllib
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
    
class Addon:
    '''
    This class provides a lot of code that is used across many XBMC addons
    in the hope that it will simplify some of the common tasks an addon needs
    to perform.
    
    Mostly this is achieved by providing a wrapper around commonly used parts
    of :mod:`xbmc`, :mod:`xbmcaddon`, :mod:`xbmcgui` and :mod:`xbmcplugin`. 
    
    You probably want to have exactly one instance of this class in your addon
    which you can call from anywhere in your code.
    
    Example::
        
        import sys
        from t0mm0.common.addon import Addon
        addon = Addon('my.plugin.id', argv=sys.argv)
    '''
    
        
    def __init__(self, addon_id, argv=None):
        '''        
        Args:
            addon_id (str): Your addon's id (eg. 'plugin.video.t0mm0.test').
            
        Kwargs:
            argv (list): List of arguments passed to your addon if applicable
            (eg. sys.argv).
        '''
        self.addon = xbmcaddon.Addon(id=addon_id)
        if argv:
            self.url = argv[0]
            self.handle = int(argv[1])
            self.queries = self.parse_query(argv[2][1:])
        

    def get_author(self):
        '''Returns the addon author as defined in ``addon.xml``.'''
        return self.addon.getAddonInfo('author')
            

    def get_changelog(self):    
        '''Returns the addon changelog.'''
        return self.addon.getAddonInfo('changelog')
            

    def get_description(self):
        '''Returns the addon description as defined in ``addon.xml``.'''
        return self.addon.getAddonInfo('description')
            

    def get_disclaimer(self):    
        '''Returns the addon disclaimer as defined in ``addon.xml``.'''
        return self.addon.getAddonInfo('disclaimer')
            

    def get_fanart(self):
        '''Returns the full path to the addon fanart.'''
        return self.addon.getAddonInfo('fanart')
            

    def get_icon(self):
        '''Returns the full path to the addon icon.'''
        return self.addon.getAddonInfo('icon')
            

    def get_id(self):
        '''Returns the addon id as defined in ``addon.xml``.'''
        return self.addon.getAddonInfo('id')
            

    def get_name(self):    
        '''Returns the addon name as defined in ``addon.xml``.'''
        return self.addon.getAddonInfo('name')
            

    def get_path(self):
        '''Returns the full path to the addon directory.'''
        return self.addon.getAddonInfo('path')
            

    def get_profile(self):    
        '''
        Returns the full path to the addon profile directory 
        (useful for storing files needed by the addon such as cookies).
        '''
        return xbmc.translatePath(self.addon.getAddonInfo('profile'))
            

    def get_stars(self):    
        '''Returns the number of stars for this addon.'''
        return self.addon.getAddonInfo('stars')
            

    def get_summary(self):    
        '''Returns the addon summary as defined in ``addon.xml``.'''
        return self.addon.getAddonInfo('summary')
            

    def get_type(self): 
        '''
        Returns the addon summary as defined in ``addon.xml`` 
        (eg. xbmc.python.pluginsource).
        '''   
        return self.addon.getAddonInfo('type')
            

    def get_version(self):    
        '''Returns the addon version as defined in ``addon.xml``.'''
        return self.addon.getAddonInfo('version')
            

    def get_setting(self, setting):
        '''
        Returns an addon setting. Settings must be defined in your addon's
        ``resources/settings.xml`` file.
        
        Args:
            setting (str): Name of the setting to be retrieved.
            
        Returns:
            str containing the requested setting.
        '''
        return self.addon.getSetting(setting)
        

    def get_string(self, string_id):
        '''
        Returns a localized string. Strings must be defined in your addon's
        ``resources/language/[lang_name]/strings.xml`` file.
        
        Args:
            string_id (int): id of the translated string to retrieve.
            
        Returns:
            str containing the localized requested string.
        '''
        return self.addon.getLocalizedString(string_id)   


    def parse_query(self, query, defaults={'mode': 'main'}):
        '''
        Parse a query string as used in a URL or passed to your addon by XBMC.
        
        Example:
         
        >>> addon.parse_query('name=test&type=basic')
        {'mode': 'main', 'name': 'test', 'type': 'basic'} 
            
        Args:
            query (str): A query string.
            
        Kwargs:
            defaults (dict): A dictionary containing key/value pairs parsed 
            from the query string. If a key is repeated in the query string
            its value will be a list containing all of that keys values.  
        '''
        queries = cgi.parse_qs(query)
        q = defaults
        for key, value in queries.items():
            if len(value) == 1:
                q[key] = value[0]
            else:
                q[key] = value
        return q


    def build_plugin_url(self, queries):
        '''
        Returns a ``plugin://`` URL which can be used to call the addon with 
        the specified queries.
        
        Example:
        
        >>> addon.build_plugin_url({'name': 'test', 'type': 'basic'})
        'plugin://your.plugin.id/?name=test&type=basic'
        
        
        Args:
            queries (dict): A dctionary of keys/values to be added to the 
            ``plugin://`` URL.
            
        Retuns:
            A string containing a fully formed ``plugin://`` URL.
        '''
        return self.url + '?' + urllib.urlencode(queries)


    def log(self, msg, level=xbmc.LOGNOTICE):
        '''
        Writes a string to the XBMC log file. The addon name is inserted into 
        the beginning of the message automatically to help you find relevent 
        messages in the log file.
        
        The available log levels are defined in the :mod:`xbmc` module and are
        currently as follows::
        
            xbmc.LOGDEBUG = 0
            xbmc.LOGERROR = 4
            xbmc.LOGFATAL = 6
            xbmc.LOGINFO = 1
            xbmc.LOGNONE = 7
            xbmc.LOGNOTICE = 2
            xbmc.LOGSEVERE = 5
            xbmc.LOGWARNING = 3
        
        Args:
            msg (str or unicode): The message to be written to the log file.
        
        Kwargs:
            level (int): The XBMC log level to write at.
        '''
        msg = unicodedata.normalize('NFKD', unicode(msg)).encode('ascii',
                                                                 'ignore')
        xbmc.log('%s: %s' % (self.get_name(), msg), level)
        

    def log_error(self, msg):
        '''
        Convenience method to write to the XBMC log file at the 
        ``xbmc.LOGERROR`` error level. Use when something has gone wrong in
        your addon code. This will show up in the log prefixed with 'ERROR:'
        whether you have debugging switched on or not.
        '''
        self.log(msg, xbmc.LOGERROR)    
        

    def log_debug(self, msg):
        '''
        Convenience method to write to the XBMC log file at the 
        ``xbmc.LOGDEBUG`` error level. Use this when you want to print out lots 
        of detailed information that is only usefull for debugging. This will 
        show up in the log only when debugging is enabled in the XBMC settings,
        and will be prefixed with 'DEBUG:'.
        '''
        self.log(msg, xbmc.LOGDEBUG)    


    def log_notice(self, msg):
        '''
        Convenience method to write to the XBMC log file at the 
        ``xbmc.LOGNOTICE`` error level. Use for general log messages. This will
        show up in the log prefixed with 'NOTICE:' whether you have debugging 
        switched on or not.
        '''
        self.log(msg, xbmc.LOGNOTICE)    


    def show_ok_dialog(self, msg, title=None, is_error=False):
        '''
        Display an XBMC dialog with a message and a single 'OK' button. The 
        message is also written to the XBMC log file at the appropriate log
        level.
        
        .. warning::
            
            Don't forget that `msg` must be a list of strings and not just a 
            string even if you only want to display a single line!
        
        Example::
        
            addon.show_ok_dialog(['My message'], 'My Addon')
        
        Args:
            msg (list of strings): The message to be displayed in the dialog. 
            Only the first 3 list items will be displayed.
            
        Kwargs:
            title (str): String to be displayed as the title of the dialog box.
            Defaults to the addon name.
            
            is_error (bool): If ``True``, the log message will be written at 
            the ERROR log level, otherwise NOTICE will be used.
        '''
        if not title:
            title = self.get_name()
        log_msg = ' '.join(msg)
        
        while len(msg) < 3:
            msg.append('')
        
        if is_error:
            self.log_error(log_msg)
        else:
            self.log_notice(log_msg)
        
        xbmcgui.Dialog().ok(title, msg[0], msg[1], msg[2])


    def show_error_dialog(self, msg):
        '''
        Convenience method to show an XBMC dialog box with a single OK button
        and also write the message to the log file at the ERROR log level.
        
        The title of the dialog will be the addon's name with the prefix 
        'Error: '.
        
        .. warning::
            
            Don't forget that `msg` must be a list of strings and not just a 
            string even if you only want to display a single line!

        Args:
            msg (list of strings): The message to be displayed in the dialog. 
            Only the first 3 list items will be displayed.
        '''
        self.show_ok_dialog(msg, 'Error: %s' % self.get_name(), True)


    def show_small_popup(self, title='', msg='', delay=5000, image=''):
        '''
        Displays a small popup box in the lower right corner. The default delay 
        is 5 seconds.

        Code inspired by anarchintosh and daledude's Icefilms addon.

        Example::

            import os
            logo = os.path.join(addon.get_path(), 'art','logo.jpg')
            addon.show_small_popup('MyAddonName','Is now loaded enjoy', 5000, logo)

        Kwargs:
            title (str): title to be displayed at the top of the box
            
            msg (str): Main message body
            
            delay (int): delay in milliseconds until it disapears
            
            image (str): Path to the image you want to display
        '''
        xbmc.executebuiltin('XBMC.Notification("%s","%s",%d,"%s")' %
                            (title, msg, delay, image))
        

    def show_settings(self):
        '''Shows the settings dialog for this addon.'''
        self.addon.openSettings()


    def resolve_url(self, stream_url):
        '''
        Tell XBMC that you have resolved a URL (or not!).
        
        This method should be called as follows:
        
        #. The user selects a list item that has previously had ``isPlayable``
           set (this is true for items added with :meth:`add_item`, 
           :meth:`add_music_item` or :meth:`add_music_item`)
        #. Your code resolves the item requested by the user to a media URL
        #. Your addon calls this method with the resolved URL
        
        Args:
            stream_url (str or ``False``): If a string, tell XBMC that the 
            media URL ha been successfully resolved to stream_url. If ``False`` 
            or an empty string tell XBMC the resolving failed and pop up an 
            error messsage.
        '''
        if stream_url:
            self.log_debug('resolved to: %s' % stream_url)
            xbmcplugin.setResolvedUrl(self.handle, True, 
                                      xbmcgui.ListItem(path=stream_url))
        else:
            self.show_error_dialog(['sorry, failed to resolve URL :('])
            xbmcplugin.setResolvedUrl(self.handle, False, xbmcgui.ListItem())

    
    def get_playlist(self, pl_type, new=False):
        '''
        Return a :class:`xbmc.Playlist` object of the specified type.
        
        The available playlist types are defined in the :mod:`xbmc` module and 
        are currently as follows::
        
            xbmc.PLAYLIST_MUSIC = 0
            xbmc.PLAYLIST_VIDEO = 1
            
        .. seealso::
            
            :meth:`get_music_playlist`, :meth:`get_video_playlist`
            
        Args:
            pl_type (int): The type of playlist to get.
            
            new (bool): If ``False`` (default), get the current 
            :class:`xbmc.Playlist` object of the type specified. If ``True`` 
            then return a new blank :class:`xbmc.Playlist`.

        Returns:
            A :class:`xbmc.Playlist` object.
        '''
        pl = xbmc.PlayList(pl_type)
        if new:
            pl.clear()
        return pl
    
    
    def get_music_playlist(self, new=False):
        '''
        Convenience method to return a music :class:`xbmc.Playlist` object.
        
        .. seealso::
        
            :meth:`get_playlist`
        
        Kwargs:
            new (bool): If ``False`` (default), get the current music 
            :class:`xbmc.Playlist` object. If ``True`` then return a new blank
            music :class:`xbmc.Playlist`.
        Returns:
            A :class:`xbmc.Playlist` object.
       '''
        self.get_playlist(xbmc.PLAYLIST_MUSIC, new)
    

    def get_video_playlist(self, new=False):
        '''
        Convenience method to return a video :class:`xbmc.Playlist` object.
        
        .. seealso::
        
            :meth:`get_playlist`
        
        Kwargs:
            new (bool): If ``False`` (default), get the current video 
            :class:`xbmc.Playlist` object. If ``True`` then return a new blank
            video :class:`xbmc.Playlist`.
            
        Returns:
            A :class:`xbmc.Playlist` object.
        '''
        self.get_playlist(xbmc.PLAYLIST_VIDEO, new)


    def add_item(self, play, infolabels, img='', fanart='', resolved=False, 
                 total_items=0, playlist=False, item_type='video', cm=None):
        '''
        Adds an item to the list of entries to be displayed in XBMC or to a 
        playlist.
        
        Use this method when you want users to be able to select this item to
        start playback of a media file. You can either pass the direct URL to
        the media file (in which case you must also set ``resolved=True``) or
        some other string that will be passed as the 'play' query and can be  
        used by the addon to resolve to a real media URL. 
        
        .. seealso::
        
            :meth:`add_music_item`, :meth:`add_video_item`, 
            :meth:`add_directory`
            :meth:`ContextMenu`
            
        Args:
            play (str): The string to be sent to the plugin when the user 
            plays this entry, or (if ``resolved=True``) a URL to the media to be
            played.
            
            infolabels (dict): A dictionary of information about this media 
            (see the `XBMC Wiki InfoLabels entry 
            <http://wiki.xbmc.org/?title=InfoLabels>`_).
            
        Kwargs:
            img (str): A URL to an image file to be used as an icon for this
            entry.
            
            fanart (str): A URL to a fanart image for this entry.
            
            resolved (bool): If ``False`` (default), `play` will be sent as a 
            query to the addon when the item is played. If ``False``, `play` 
            will be treated as a URL to the media item.
            
            total_items (int): Total number of items to be added in this list.
            If supplied it enables XBMC to show a progress bar as the list of
            items is being built.
            
            playlist (playlist object): If ``False`` (default), the item will 
            be added to the list of entries to be displayed in this directory. 
            If a playlist object is passed (see :meth:`get_playlist`) then 
            the item will be added to the playlist instead
    
            item_type (str): The type of item to add (eg. 'music', 'video' or
            'pictures')
            
            cm (obj): The ContextMenu object where you have set either favorite
            or context or both. 

            See :meth: 'ContextMenu' for more information.
        '''
        menuobj = None
        if cm is not None:
            scriptargs = {'mode' : cm.favorite['action'], 
                          'title' : infolabels['title'], 
                          'callback' : cm.favorite['callback'], 'url' : play,
                          'item_type' : item_type, 'img' : img, 
                          'fanart' : fanart, 'favtype' : cm.favorite['favtype']}

            cm.add_context(cm.favorite['menuname'], scriptargs, False)
            menuobj = cm._generate_menu()

        infolabels = self.unescape_dict(infolabels)
        if not resolved:
            play = self.build_plugin_url({'play': play})
        listitem = xbmcgui.ListItem(infolabels['title'], iconImage=img, 
                                    thumbnailImage=img)
        listitem.setInfo(item_type, infolabels)
        listitem.setProperty('IsPlayable', 'true')
        listitem.setProperty('fanart_image', fanart)
        if menuobj is not None:
            listitem.addContextMenuItems(menuobj)
        if playlist is not False:
            self.log_debug('adding item: %s - %s to playlist' % \
                                                    (infolabels['title'], play))
            playlist.add(play, listitem)
        else:
            self.log_debug('adding item: %s - %s' % (infolabels['title'], play))
            xbmcplugin.addDirectoryItem(self.handle, play, listitem, 
                                        isFolder=False, totalItems=total_items)


    def add_video_item(self, play, infolabels, img='', fanart='', 
                       resolved=False, total_items=0, playlist=False, cm=None):
        '''
        Convenience method to add a video item to the directory list or a 
        playlist.
        
        See :meth:`add_item` for full infomation
        '''
        self.add_item(play, infolabels, img, fanart, resolved, total_items, 
                      playlist, item_type='video', cm=cm)


    def add_music_item(self, play, infolabels, img='', fanart='', 
                       resolved=False, total_items=0, playlist=False, cm=None):
        '''
        Convenience method to add a music item to the directory list or a 
        playlist.
        
        See :meth:`add_item` for full infomation
        '''
        self.add_item(play, infolabels, img, fanart, resolved, total_items, 
                      playlist, item_type='music', cm=cm)


    def add_directory(self, queries, title, img='', fanart='', 
                      total_items=0, is_folder=True, cm=None):
        '''
        Add a directory to the list of items to be displayed by XBMC.
        
        When selected by the user, directory will call the addon with the 
        query values contained in `queries`.
        
        Args:
            queries (dict): A set of keys/values to be sent to the addon when 
            the user selects this item.
            
            title (str): The name to be displayed for this entry.
        
        Kwargs:
            img (str): A URL to an image file to be used as an icon for this
            entry.
            
            fanart (str): A URL to a fanart image for this entry.
            
            total_items (int): Total number of items to be added in this list.
            If supplied it enables XBMC to show a progress bar as the list of
            items is being built.

            is_folder (bool): if ``True`` (default), when the user selects this 
            item XBMC will expect the plugin to add another set of items to 
            display. If ``False``, the 'Loading Directory' message will not be
            displayed by XBMC (useful if you want a directory item to do 
            something like pop up a dialog).
            
            cm (obj): The ContextMenu object where you have set either favorite
            or context or both. e.g ContextMenu.add_context()
            
            See :meth: 'ContextMenu' for more information.
        '''
        menuobj = None
        if cm is not None:
            # TODO: work around dict_to_string
            if cm.favorite is not None:
                querystring = self.dict_to_string(queries)
                #querystring = self.parse_query(queries, defaults={})
                scriptargs = {'mode' : cm.favorite['action'], 'title' : title,
                              'callback' : cm.favorite['callback'], 
                              'img' : img, 'fanart' : fanart, 
                              'queries' : base64.urlsafe_b64encode(querystring),
                              'favtype' : cm.favorite['favtype'] }
                           
                cm.add_context(cm.favorite['menuname'], scriptargs, False)
            menuobj = cm._generate_menu()

            
        url = self.build_plugin_url(queries)
        title = self.unescape(title)
        self.log_debug(u'adding dir: %s - %s' % (title, url))
        listitem = xbmcgui.ListItem(title, iconImage=img, 
                                    thumbnailImage=img)
        if menuobj is not None:
            listitem.addContextMenuItems(menuobj)
        if not fanart:
            fanart = self.get_fanart()
        listitem.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(self.handle, url, listitem, 
                                    isFolder=is_folder, totalItems=total_items)


    def end_of_directory(self):
        '''Tell XBMC that we have finished adding items to this directory.'''
        xbmcplugin.endOfDirectory(self.handle)
        

    def _decode_callback(self, matches):
        '''Callback method used by :meth:`decode`.'''
        id = matches.group(1)
        try:
            return unichr(int(id))
        except:
            return id
            

    def decode(self, data):
        '''
        Regular expression to convert entities such as ``&#044`` to the correct
        characters. It is called by :meth:`unescape` and so it is not required
        to call it directly.
        
        This method was found `on the web <http://stackoverflow.com/questions/1208916/decoding-html-entities-with-python/1208931#1208931>`_
        
        Args:
            data (str): String to be cleaned.
            
        Returns:
            Cleaned string.
        '''
        return re.sub("&#(\d+)(;|(?=\s))", self._decode_callback, data).strip()


    def unescape(self, text):
        '''
        Decodes HTML entities in a string.
        
        You can add more entities to the ``rep`` dictionary.
        
        Args:
            text (str): String to be cleaned.
            
        Returns:
            Cleaned string.
        '''
        text = self.decode(text)
        rep = {'&lt;': '<',
               '&gt;': '>',
               '&quot': '"',
               '&rsquo;': '\'',
               '&acute;': '\'',
               }
        for s, r in rep.items():
            text = text.replace(s, r)
        # this has to be last:
        text = text.replace("&amp;", "&")
        return text
        

    def unescape_dict(self, d):
        '''
        Calls :meth:`unescape` on all values in a dictionary.
        
        Args:
            d (dict): A dictionary containing string values
            
        Returns:
            A dictionary with HTML entities removed from the values.
        '''
        out = {}
        for key, value in d.items():
            out[key] = self.unescape(value)
        return out
    
    def save_data(self, filename, data):
        '''
        Saves the data structure using pickle. If the addon data path does 
        not exist it will be automatically created. This save function has
        the same restrictions as the pickle module.
        
        Args:
            filename (string): name of the file you want to save data to. This 
            file will be saved in your addon's profile directory.
            
            data (data object/string): you want to save.
            
        Returns:
            True on success
            False on failure
        '''
        profile_path = self.get_profile()
        try:
            os.makedirs(profile_path)
        except:
            pass
        save_path = os.path.join(profile_path, filename)
        try:
            pickle.dump(data, open(save_path, 'wb'))
            return True
        except pickle.PickleError:
            return False
        return True
        
    def load_data(self,filename):
        '''
        Load the data that was saved with save_data() and returns the
        data structure.
        
        Args:
            filename (string): Name of the file you want to load data from. This
            file will be loaded from your addons profile directory.
            
        Returns:
            Data stucture on success
            False on failure
        '''
        profile_path = self.get_profile()
        load_path = os.path.join(profile_path, filename)
        print profile_path
        if not os.path.isfile(load_path):
            self.log_debug('%s does not exist' % load_path)
            return False
        try:
            data = pickle.load(open(load_path))
        except:
            return False
        return data

            
    def save_favorite(self):
        '''
        This function should ONLY be called from mode == 'savefavorite', as
        it expects the particular data structure from the "save menu". If
        you need to save your own data in a fast way use save_data()
        
        See :meth:`load_data` for infomation.
        
            
        '''
        savedata={}
        for key in self.queries:
            match = re.match(r'([\d|\w|\s]+)', key)
            if match:
                savedata[key] = self.queries[key]
        filename = base64.urlsafe_b64encode(savedata['title'])
        profile_path = self.get_profile()
        try:
            os.makedirs(profile_path)
        except:
            pass
        favorite_path = os.path.join(profile_path, 'Favorites')
        try:
            os.makedirs(favorite_path)
        except:
            pass
        filepath = os.path.join('Favorites', filename + '.txt')
        return self.save_data(filepath, savedata)
        
        
    def del_favorite(self):
        '''
        Takes no arguments, but expects to be called by the contextmenu
        'Delete favorite as that generates particular data required
        to delete the saved favorite.
        
        Do not call this directly, except from "mode = 'deletefavorite'"
         
        '''
        profile_path = self.get_profile()
        favorite_path = os.path.join(profile_path, 'Favorites')
        filename = base64.urlsafe_b64encode(self.queries['title'])
        filepath = os.path.join(favorite_path, filename + '.txt')
        try:
            os.remove(filepath)
        except:
            self.show_small_popup(msg='Unable to delete favorite')
            return False
        xbmc.executebuiltin("container.Refresh")
    
    
    def show_favorites(self, cm, catagories=''):
        '''
        This called when the user clicks on the favorite menu, and will present
        the user with a directory of catagories.

        Kwargs:
            catagories (dict): 
            (Default: {'movies' : 'Movies', 'tv' : 'TV Shows'} The key is the 
            favtype (or you can call it filter), and the value is what is shown
            to the user on the screen.
            
            You can overwrite the defaults to suit your addon's catagories, just
            remember that they must match your favtype that you used in
            create_favorite
            
            See :meth:`create_favorite` more infomation.
        
        '''
        if not catagories:
            catagories = { 'movies' : 'Movies', 'tv' : 'Tv shows'}
        if not 'favtype' in self.queries:
            for key in catagories:
                self.add_directory({ 'mode' : 'showfavorites',
                                     'favtype' : key }, catagories[key])
            return
        profile_path = self.get_profile()
        favoritefolder = os.path.join(profile_path,'Favorites')
        try:
            allfiles=os.listdir(favoritefolder)
        except:
            self.show_small_popup(msg='No favorites saved')
            return False
        for filename in allfiles:
            print filename
            filepath = os.path.join('Favorites', filename)
            data = self.load_data(filepath)
            if data:
                if re.match(data['favtype'], self.queries['favtype'], re.I):
                    cm.add_favorite('Delete favorite',
                                { 'mode' : 'deletefavorite'}, 'deletefavorite', 
                                self.queries['favtype'] )
                    if data['callback'] == 'play':
                        self.add_item(data['url'], { 'title' : data['title']}, 
                                      item_type=data['item_type'], cm=cm)
                    else:
                        unencoded = base64.urlsafe_b64decode(data['queries'])
                        # TODO: Work around string_to_dict
                        queries = self.string_to_dict(unencoded)
                        #queries = urllib.urlencode(unencoded)
                        self.add_directory(queries, data['title'], cm=cm)
            else:
                return False
        
            
    def dict_to_string(self, dictionary):
        ''' 
        This is a convinient way to convert a dictionary to a string. It can 
        only be 2 layers deep e.g. 
        
        { 'mylist' : ('foo', 'bar', 'chimera'), 'mydict' : { 'key1' : 'key1value',
         'key2' : 'key2value' }, 'myurl' : 'http://xmbx.org' }

        Args:
            dictionary (dict): Each value in the dict can contain one of the 
            following: bol, Nontype, str, dict, list, tuple, int. Note that the 
            dict in dict, list in dict, tuple in dict's contents must be
            one of the above types, also any int values will have become
            str values, and you need to set it again after using string_to_dict.
            
            See :meth:`string_to_dict` for infomation.
            
        Returns:
            A string in the format &key=value, how ever it's not url safe.
        
        '''
        dictstring = ''
        for key in dictionary:
            string = key
            m = re.match(r'([\d|\w|\s]+)', string)
            if m:
                if type(dictionary[key]) == tuple:
                    tuplestring = '&%s=%s' % (key,'__tuple__/')
                    for value in dictionary[key]:
                        tuplestring = tuplestring + '__%s' % (value)
                    dictstring = dictstring + tuplestring
                elif type(dictionary[key]) == list:
                    liststring = '&%s=%s' % (key,'__list__/')
                    for value in dictionary[key]:
                        liststring = liststring + '__%s' % (value)
                    dictstring = dictstring + liststring
                elif type(dictionary[key]) == dict:
                    dictstring = '&%s=%s' % (key, '__dict__/')
                    for middlekey in dictionary[key]:
                        dictstring = dictstring + '___%s__%s' % \
                        (middlekey, dictionary[key][middlekey])
                    dictstring = dictstring + dictstring
                else:
                    dictstring = dictstring + '&%s=__str__/%s' % \
                    (key, dictionary[key])
        return dictstring
    
    

        
        
    def string_to_dict(self, dictstring):
        '''
        This function rebuilts a dict that was previously turned into a string
        using dict_to_string. Remember as it was turned into a string the 
        values and keys are all str now.
        
        Args:
            dictstring (str): A string priveously generated by dict_to_string.
            
            See :meth:`dict_to_string` for further infomation.
        
        Returns:
            A rebuilt dictionary
        '''
        restoreddict = {}
        splitter=re.split('&', dictstring)
        for string in splitter:
            if re.match('.+?__str__/', string):
                key, value = re.split('=__str__/', string)
                restoreddict[key] = value
            elif re.match('.+?__tuple__/', string):
                key, values = re.split('=__tuple__/', string)
                splits = re.split('__', values)
                splits.pop(0)
                tmptuple = tuple(splits)
                restoreddict[key] = tmptuple
            elif re.match('.+?__list__/', string):
                key, values = re.split('=__list__/', string)
                splits = re.split('__', values)
                splits.pop(0)
                restoreddict[key] = splits
            elif re.match('.+?__dict__/', string):
                tmpdict = {}
                key, values = re.split('=__dict__/', string)
                entrypairs = re.split('___', values)
                for pair in entrypairs:
                    if pair:
                        pairkey, pairvalue = re.split('__', pair)
                        tmpdict[pairkey] = pairvalue
                restoreddict[key] = tmpdict
        return restoreddict

class ContextMenu:
    
    def __init__(self, addon_url):
        '''
        This class allows you to add menu's that will be displayed when the 
        user right clicks on the movie or directory. It handles all the
        background for you, and allows you to consentrate on coding your addon.
        
        Usage:
        In order to use the built-in favorite setup there is a few lines
        that must be added to your addon.
        
        First: Import and initiate the Addon and ContextMenu classes.
        from t0mm0.common.addon import Addon
        from t0mm0.common.addon import ContextMenu
        addon = Addon('plugin.video.solarmovie', sys.argv)
        cm = ContextMenu(addon.url)
        
        Second: Add the following lines to your addon, just above 'if not play:'
        elif mode == 'savefavorite':
            success = addon.save_favorite()
            if success is False:
                addon.show_small_popup(msg='Unable to save favorite')
            else:
                addon.show_small_popup(msg='Favorite saved')
    
    
        elif mode == 'deletefavorite':
            addon.del_favorite()
            
            
        elif mode == 'showfavorites':
            addon.show_favorites(cm)
            
            
        Third: Where you want to have the Favorites menu display add this line.
        add_directory({'mode' : 'showfavorites' }, 'Favorites')
            
        For information on how to add the favorite context menu to your links
        or directories, please see the links below
        
        See :meth:`add_context` on how to add your own menu's
        See :meth:`add_favorite` on how to add the favorite menu.
        See :meth:`add_dir` on how to apply the menu to a directory
        See :meth:`add_item` on how to apply the menu on an item (movie, song).
            
        Args:
            addon_url (str): from addon.url
        '''
        self.contextmenu = {}
        self.favorite = None
        self.addonurl = addon_url
        
        
    def add_context(self, menuname, scriptargs, newlist=False):
        '''
        Lets you create a context menu, that will be applied when you provide
        the ContextMenu object to the add_dir, add_item, add_video_item,
        and add_music_item.
        
        args:
            menuname (str): The name that will be shown in your menu
            
            scriptargs (dict): consiting of key / value to be used as arguments
            for the call when the menu is clicked e.g. { 'mode' : 'main' }.
                
        kwargs:
            newlist (Bol): Default False, If you want to replace the current 
            movie / dir list shown on the screen set this to True.
            If you want to do some background tasks, and have the the user stay
            on the same screen, set this to False or omit.
        '''
        encodedscriptargs = urllib.urlencode(scriptargs)
        self.contextmenu[menuname] = {'menuname' : menuname,
                                      'encodedscriptargs' : encodedscriptargs,
                                      'newlist' : newlist}

    
    
    def add_favorite(self, menuname, callback, action='savefavorite', 
                     favtype='movies', ):
        '''
        add_favorite is used to apply a favorite menu item to an item or dir.
        Once that is done, you can pass the ContextMenu object to the add_dir,
        add_video_item, add_music_item, and add_item, to have that menu context
        set.

        Args:
            menuname (string): The name displayed as the menu item, e.g.
            'Save Myaddon Favorite'
            
            callback (dict): This is the mode that will be 
            called when the user clicks on a shown favorite. It can be a 
            mode defined in your addon or play.
            
            e.g. { 'mode' : 'play' } or { 'mode' : 'findmovielinks' }
            
        Kwargs:
            action (string): (Default: savefavorite) This is the function that
            will be called when the user clicks on the menu item. It should
            not be cahnged as the favorite module takes care of this.
            
            favtype (string): (Default: movie) This is used as a sort function
            when the favorite is displayed. It will put the saved favorites
            into catagories.
            
            See :meth:`show_favorites` for infomation on catagories
            

        '''
        if not menuname:
            menuname = 'Add as favorite in this addon'
        self.favorite = { 'callback' : callback['mode'], 'action' : action, 
                         'favtype' : favtype, 'menuname' : menuname }
    

    def _generate_menu(self):
        '''
        This will take the stored context menu's added with add_contextmenu
        and add_favorite, and create the object that xbmc expects to see in 
        order to apply menu's. This is all handled in the add_dir and add_item
        functions in Addon.
        
        Do not call this directly.
        
        
        '''
        menulist = []
        for key in self.contextmenu:
            if self.contextmenu[key]['newlist']:
                menulist.append((key, u'XBMC.Container.Update(%s/?%s)' % 
                                (self.addonurl, 
                                 self.contextmenu[key]['encodedscriptargs'] )))
            else:
                menulist.append((key, u'XBMC.RunPlugin(%s/?%s)' % 
                                (self.addonurl, 
                                 self.contextmenu[key]['encodedscriptargs'] )))
        return menulist

            