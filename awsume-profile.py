"""
Add the following to iterm2_print_user_vars

iterm2_set_user_var awsProfile $AWSUME_PROFILE
"""

import iterm2

async def main(connection):
    component = iterm2.StatusBarComponent(
        short_description='AWSume Profile',
        detailed_description='The AWS profile as configured by awsume',
        exemplar='AWSume Profile',
        update_cadence=2,
        identifier='com.ironhalo.iterm-statusbar.awsume-profile',
        knobs=[],
    )

    @iterm2.StatusBarRPC
    async def awsume_profile(knobs, profile=iterm2.Reference('user.awsProfile?')):
        if profile:
            return f'aws: {profile}'
        else:
            return f''

    await component.async_register(connection, awsume_profile)
iterm2.run_forever(main)
