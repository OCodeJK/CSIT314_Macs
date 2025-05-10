from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from control.CleanerConfirmedMatchesController import CleanerConfirmedMatchesController

# Create the blueprint instance
confirmed_matches_bp = Blueprint('confirmed_matches', __name__)

class CleanerConfirmedMatchesPg:
    def __init__(self):
        self.controller = CleanerConfirmedMatchesController()




# Flask routes
@confirmed_matches_bp.route('/cleaner/confirmed-matches', methods=['GET'])
def display_matches():
    """
    Display all confirmed matches for a cleaner
    """
    try:
        cleaner_id = request.args.get('cleaner_id', '1')
        
        # Initialize boundary class
        page_handler = CleanerConfirmedMatchesPg()
        
        # Use controller to get matches
        matches = page_handler.controller.cleanerViewMatches(cleaner_id)
        
        # Format results for display
        formatted_matches = []
        if matches:
            for match in matches:
                formatted_match = {
                    'matchId': match[0],
                    'serviceId': match[1],
                    'date': match[2],  # This is startDate in the database
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
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(error=str(e)), 500
        flash(f"An error occurred while loading confirmed matches: {str(e)}", "error")
        return redirect(url_for('home'))

@confirmed_matches_bp.route('/cleaner/match-details/<match_id>', methods=['GET'])
def view_match_details(match_id):
    """
    View details of a specific match
    """
    try:
        cleaner_id = request.args.get('cleaner_id', '1')
        
        # Initialize boundary class
        page_handler = CleanerConfirmedMatchesPg()
        
        # Get match details
        match = page_handler.controller.getMatchDetails(match_id, cleaner_id)
        
        if not match:
            flash("Match not found or you don't have permission to view it", "error")
            return redirect(url_for('confirmed_matches.display_matches', cleaner_id=cleaner_id))
        
        # Format match for template
        formatted_match = {
            'matchId': match[0],
            'serviceId': match[1],
            'startDate': match[2],
            'endDate': match[3],
            'cleanerId': match[4],
            'serviceName': match[5] if len(match) > 5 else 'Unknown Service'
        }
        
        return render_template(
            'match_details.html',
            cleaner_id=cleaner_id,
            match=formatted_match
        )
    except Exception as e:
        print(f"Error in view_match_details: {str(e)}")
        flash(f"An error occurred while loading match details: {str(e)}", "error")
        return redirect(url_for('confirmed_matches.display_matches', cleaner_id=cleaner_id))
