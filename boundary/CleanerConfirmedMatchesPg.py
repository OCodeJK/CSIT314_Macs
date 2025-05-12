from flask import Blueprint, render_template, request, redirect, flash
from control.CleanerConfirmedMatchesController import CleanerConfirmedMatchesController

# Create the blueprint instance
confirmed_matches_bp = Blueprint('confirmed_matches', __name__)

class CleanerConfirmedMatchesPg:
    def __init__(self):
        self.controller = CleanerConfirmedMatchesController()

page_handler = CleanerConfirmedMatchesPg()


@confirmed_matches_bp.route('/cleaner/confirmed-matches', methods=['GET'])
def display_matches():
    """
    Display all confirmed matches for a cleaner
    """
    try:
        cleaner_id = request.args.get('cleaner_id', '1')
        
        matches = page_handler.controller.cleanerViewMatches(cleaner_id)
        
        formatted_matches = []
        if matches:
            for match in matches:
                formatted_match = {
                    'matchId': match[0],
                    'serviceId': match[1],
                    'date': match[2],  # startDate in database
                    'serviceName': match[5] if len(match) > 5 else 'Unknown Service'
                }
                formatted_matches.append(formatted_match)

        return render_template(
            'confirmed_matches.html', 
            cleaner_id=cleaner_id,
            matches=formatted_matches
        )
    except Exception as e:
        print(f"Error in display_matches: {str(e)}")
        flash(f"An error occurred while loading confirmed matches: {str(e)}", "error")
        return redirect('/services/' + cleaner_id)

@confirmed_matches_bp.route('/cleaner/match-details/<match_id>', methods=['GET'])
def view_match_details(match_id):
    """
    View details of a specific match
    """
    try:
        cleaner_id = request.args.get('cleaner_id', '1')
        

        match = page_handler.controller.getMatchDetails(match_id, cleaner_id)
        
        if not match:
            flash("Match not found or you don't have permission to view it", "error")
            return redirect('/cleaner/confirmed-matches?cleaner_id=' + cleaner_id)
        
        formatted_match = {
            'matchId': match[0],
            'serviceId': match[1],
            'startDate': match[2].strftime('%Y-%m-%d') if hasattr(match[2], 'strftime') else match[2],
            'endDate': match[3].strftime('%Y-%m-%d') if match[3] and hasattr(match[3], 'strftime') else match[3],
            'cleanerId': match[4],
            'serviceName': match[5] if len(match) > 5 else 'Unknown Service',
            'categoryName': match[6] if len(match) > 6 else 'Unknown Category',
            'price': match[7] if len(match) > 7 else 0.0,
            'viewCount': match[8] if len(match) > 8 else 0
        }
        
        return render_template(
            'match_details.html',
            cleaner_id=cleaner_id,
            match=formatted_match
        )
    except Exception as e:
        print(f"Error in view_match_details: {str(e)}")
        flash(f"An error occurred while loading match details: {str(e)}", "error")
        return redirect('/cleaner/confirmed-matches?cleaner_id=' + cleaner_id)