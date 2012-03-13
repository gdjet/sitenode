from setuptools import setup, find_packages

setup(
    name='sitenode',
    version='0.99.7',
    description='Basic Models for Web Development',
    author='g4b',
    author_email='gab(at)g4b.org',
    url='',
    download_url='',
    install_requires=['django-tinymce', 'django-endless-pagination',
                      'django-grappelli', 'django-filebrowser>=3.4.0',
                      'markdown'],
    #requires=['django-tinymce', 'django-endless-pagination',
    #                  'django-grappelli', 'django-filebrowser>=3.4.0'],
    package_dir={'': 'src'},
    packages=find_packages('src/'),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
