import re
import json
import datetime
from copy import deepcopy
from juicer.items import *
import MySQLdb

from json_validator import validate_json_record


SOURCES_LIST = {}


class JuicerPipeline(object):

    def get_source(self, spider):
        return spider.name.split('_', 1)[0].strip()


    def write_item_into_avail_file(self, item, spider, content_type):
        source = self.get_source(spider)

        if SOURCES_LIST.has_key(source):
            SOURCES_LIST[source](item, spider.get_avail_file(), spider.get_json_file())

    def process_item(self, item, spider):
        if isinstance(item, BestSellers):
            best_seller_values = '#<>#'.join([
                item['product_id'],item.get('name',''), item.get('no_of_reviews', ''),  item.get('star_rating', ''),item.get('price', ''),item.get('rank',''),item.get('week_number', ''),item.get('category', ''), item.get('is_prime', ''),item.get('product_url', ''),item.get('reference_url', '')
            ])
            spider.get_bestsellers_file().write('%s\n' %best_seller_values)
            spider.get_bestsellers_file().flush()

            self.write_item_into_avail_file(item, spider, 'bestseller')

        if isinstance(item, Products):
            product_values = '#<>#'.join([
                item['id'],item.get('name',''), item.get('original_price',''), item.get('discount_price',''), item.get('features', ''),  item.get('description', ''),item.get('item_number', ''),item.get('date_available',''),item.get('best_sellerrank', ''),str(item.get('aux_info', '')),item.get('reference_url', '')
            ])
            spider.get_products_file().write('%s\n' %product_values)
            spider.get_products_file().flush()

            self.write_item_into_avail_file(item, spider, 'products')

        if isinstance(item, RelatedSellers):
            relatedsellers_values = '#<>#'.join([
                item['related_sk'],item.get('product_id',''), item.get('name', ''),  item.get('category', ''),item.get('product_condition', ''),item.get('seller_name',''),item.get('seller_no_of_rating', ''),item.get('seller_rating_percentage', ''),item.get('seller_price',''),item.get('is_prime', ''),str(item.get('aux_info', ''))
            ])
            spider.get_relatedsellers_file().write('%s\n' %relatedsellers_values)
            spider.get_relatedsellers_file().flush()

            self.write_item_into_avail_file(item, spider, 'relatedsellers')
        if isinstance(item, RichMedia):
            richmedia_values = '#<>#'.join([
                item['sk'],item.get('product_id',''), item.get('category', ''),  item.get('size', ''),item.get('dimensions', ''),item.get('image_url',''),item.get('reference_url', ''),str(item.get('aux_info', ''))
            ])
            spider.get_richmedia_file().write('%s\n' %richmedia_values)
            spider.get_richmedia_file().flush()

            self.write_item_into_avail_file(item, spider, 'richmedia')
        if isinstance(item, CustomerReviews):
            customerreviews_values = '#<>#'.join([
                item['sk'],item['product_id'],item.get('name',''), item.get('reviewed_by', ''),  item.get('reviewed_on', ''),item.get('review', ''),item.get('category',''),item.get('review_url', ''),item.get('review_rating', ''),item.get('verified_purchase_flag',''),str(item.get('aux_info', ''))
            ])
            spider.get_customerreviews_file().write('%s\n' %customerreviews_values)
            spider.get_customerreviews_file().flush()

            self.write_item_into_avail_file(item, spider, 'customerreviews')
        if isinstance(item, Twitter):
            twitter_values = '#<>#'.join([
                item['sk'], item.get('screen_name',''), item.get('name',''), item.get('description',''),item.get('location',''),item.get('tweets',''),item.get('following',''),item.get('followers',''),item.get('likes',''),item.get('image',''),item.get('lists',''),item.get('timezone',''), item.get('language',''), item.get('is_verified',''), item.get('twitter_url',''), item.get('email_id',''), str(item.get('aux_info', ''))
            ])
            spider.get_twitter_file().write('%s\n' %twitter_values)
            spider.get_twitter_file().flush()
            self.write_item_into_avail_file(item, spider, 'twitter')

        if isinstance(item, Comments):
            comments_values = '#<>#'.join([
                item['sk'], item.get('review_sk',''),  item.get('comment_name',''), item.get('comment_by', ''), item.get('comment_on', ''), item.get('comment',''),item.get('comment_votes',''),str(item.get('aux_info', ''))
            ])
            spider.get_comments_file().write('%s\n' %comments_values)
            spider.get_comments_file().flush()
            self.write_item_into_avail_file(item, spider, 'comments')
        if isinstance(item, Linkedin):
            linkedin_values = '#<>#'.join([
                item['sk'], item.get('name',''), item.get('first_name',''), item.get('last_name',''), item.get('locality',''), item.get('image',''), item.get('member_url',''), item.get('mark',''), item.get('url','')
            ])
            spider.get_linkedin_file().write('%s\n' %linkedin_values)
            spider.get_linkedin_file().flush()
            self.write_item_into_avail_file(item, spider, 'linkedin')
        if isinstance(item, Linkedinpostions):
            linkedinpositions_values = '#<>#'.join([
                item['sk'], item['profile_sk'], item.get('title',''), item.get('organization','')
                ])
            spider.get_linkedinpositions_file().write('%s\n' %linkedinpositions_values)
            spider.get_linkedinpositions_file().flush()
            self.write_item_into_avail_file(item, spider, 'linkedinpositions')

        if isinstance(item, Linkedinviewers):
            linkedinviewers_values = '#<>#'.join([
                item['sk'], item['profile_sk'], item.get('title',''), item.get('viewer_url',''), item.get('viewer_name',''), item.get('viewer_headline','')
                ])
            spider.get_linkedinviewers_file().write('%s\n' %linkedinviewers_values)
            spider.get_linkedinviewers_file().flush()
            self.write_item_into_avail_file(item, spider, 'linkedinviewers')

        if isinstance(item, DoctorInfo):
            doctorinfo_values = '#<>#'.join([
                item['doctor_id'], item.get('doctor_name',''), item.get('doctor_profile_link',''), item.get('qualification',''), item.get('years_of_experience',''), item.get('specialization',''), item.get('recently_visited_for',''), item.get('rating',''), item.get('vote_count',''), item.get('feedback_count',''), item.get('location',''), item.get('address',''), item.get('consultation_fee',''), item.get('schedule_timeslot',''), item.get('doctor_image',''), item.get('clinic_names',''), item.get('clinic_images',''), item.get('location_latitude',''), item.get('location_longitude',''), item.get('region',''), item.get('fee_currency',''), item.get('booking_type',''), item.get('reference_url',''), MySQLdb.escape_string(item.get('aux_info',''))
                ])
            spider.get_doctorinfo_file().write('%s\n' %doctorinfo_values)
            spider.get_doctorinfo_file().flush()
            self.write_item_into_avail_file(item, spider,'doctorinfo')

        if isinstance(item, HospitalInfo):
            hospitalinfo_values = '#<>#'.join([
                item['hospital_id'], item.get('hospital_name', ''), item.get('hospital_link', ''), item.get('hospital_images', ''), item.get('hospital_location', ''), item.get('hospital_speciality', ''), item.get('no_of_doctors_in_hospital', ''), item.get('hospital_star_rating', ''), item.get('hospital_feedback_count', ''), item.get('hospital_practo_gurantee', ''), item.get('hospital_booking_type', ''), item.get('hospital_open_timings', ''), item.get('hospital_schedule_timeslot', ''), item.get('hospital_accredited', ''), item.get('reference_url', ''), MySQLdb.escape_string(item.get('aux_info', ''))
                ])
            spider.get_hospitalinfo_file().write('%s\n' % hospitalinfo_values)
            spider.get_hospitalinfo_file().flush()
            self.write_item_into_avail_file(item, spider,'hospitalinfo')

        if isinstance(item, HospitalMeta):
            hospitalmeta_values = '#<>#'.join([
                item['hospital_id'], item.get('hospital_name', ''), item.get('hospital_profile_link', ''), item.get('rating_count', ''), item.get('rating_value', ''), item.get('location', ''), item.get('medical_specialities', ''), item.get('number_of_doctors', ''), item.get('description', ''), item.get('no_of_beds', ''), item.get('no_of_ambulances', ''), item.get('method_of_payment', ''), item.get('address', ''), item.get('street_address', ''), item.get('locality', ''), item.get('region', ''), item.get('postal_code'),item.get('opening_timings', ''), item.get('clinic_timings', ''), item.get('amenities', ''), item.get('emergency_contact_number', ''), item.get('services', ''), item.get('longitude', ''), item.get('latitude', ''), item.get('establishment_data', ''), item.get('feedback_count', ''), item.get('awards', ''), item.get('other_centers', ''), item.get('reference_url', ''), MySQLdb.escape_string(item.get('aux_info', ''))
                ])
            spider.get_hospitalmeta_file().write('%s\n' % hospitalmeta_values)
            spider.get_hospitalmeta_file().flush()
            self.write_item_into_avail_file(item, spider,'hospitalmeta')

        if isinstance(item, HospitalDoctor):
            hospitaldoctor_values = '#<>#'.join([
                item['sk'], item.get('hospital_id', ''), item.get('doctor_id', ''), item.get('doctor_name', ''), item.get('doctor_profile_link', ''), item.get('qualification', ''), item.get('years_of_experience', ''), item.get('specialization', ''), item.get('rating', ''), item.get('vote_count', ''), item.get('feedback_count', ''), item.get('consultation_fee', ''), item.get('doctor_image', ''), item.get('doctor_practo_gurantee', ''), item.get('booking_type', ''),  item.get('doctor_monday_timing', ''),  item.get('doctor_tuesday_timing', ''),  item.get('doctor_wednesday_timing', ''),  item.get('doctor_thursday_timing', ''),  item.get('doctor_friday_timing', ''),  item.get('doctor_saturday_timing', ''),  item.get('doctor_sunday_timing', ''), item.get('doctor_on_call', ''), item.get('reference_url', ''), MySQLdb.escape_string(item.get('aux_info', ''))
                ])
            spider.get_hospitaldoctor_file().write('%s\n' % hospitaldoctor_values)
            spider.get_hospitaldoctor_file().flush()
            self.write_item_into_avail_file(item, spider,'hospitaldoctor')


        if isinstance(item, DoctorMeta):
            doctormeta_values = '#<>#'.join([
                item['sk'], item.get('doctor_id',''), item.get('doctor_name',''), item.get('doctor_profile_link',''), item.get('qualification',''), item.get('specialization',''), item.get('years_of_experience',''), item.get('medical_registration_verified',''), item.get('rating',''), item.get('vote_count',''), item.get('summary',''), item.get('latitude',''), item.get('longitude',''), item.get('services',''), item.get('specializations',''), item.get('awards_recognitions',''), item.get('education',''), item.get('memeberships',''), item.get('experience',''), item.get('registrations',''), item.get('feedback_count',''), item.get('doctor_image',''), item.get('reference_url',''), item.get('aux_info','')
                ])
            spider.get_doctormeta_file().write('%s\n' %doctormeta_values)
            spider.get_doctormeta_file().flush()
            self.write_item_into_avail_file(item, spider,'doctormeta')

        if isinstance(item, DoctorFeedback):
            doctorfeedback_values = '#<>#'.join([
                item['sk'],item.get('doctor_id',''), item.get('feedback_count',''), item.get('feedback_filters',''), item.get('feedback_name',''), item.get('feedback_like',''), item.get('feedback_publish_date',''), item.get('feeback_text',''), item.get('feedback_helpful_count',''), item.get('feedback_helpful_overallcount',''), item.get('feedback_reply',''), item.get('feedback_practice_name',''), item.get('feedback_practice_locality',''), item.get('feedback_practice_city',''), item.get('feedback_for',''), item.get('reference_url',''), item.get('aux_info','')
                ])
            spider.get_doctorfeedback_file().write('%s\n' %doctorfeedback_values)
            spider.get_doctorfeedback_file().flush()
            self.write_item_into_avail_file(item, spider,'doctorfeedback')

        if isinstance(item, HospitalFeedback):
            hospitalfeedback_values = '#<>#'.join([
                item['sk'],item.get('hospital_id',''), item.get('feedback_count',''), item.get('feedback_filters',''), item.get('feedback_name',''), item.get('feedback_like',''), item.get('feedback_publish_date',''), item.get('feedback_text',''), item.get('feedback_helpful_count',''), item.get('feedback_helpful_overallcount',''), item.get('feedback_reply',''), item.get('feedback_practice_name',''), item.get('feedback_practice_locality',''), item.get('feedback_practice_city',''), item.get('feedback_for',''), item.get('reference_url',''), item.get('aux_info','')
                ])
            spider.get_hospitalfeedback_file().write('%s\n' % hospitalfeedback_values)
            spider.get_hospitalfeedback_file().flush()
            self.write_item_into_avail_file(item, spider,'hospitalfeedback')

        if isinstance(item, DoctorHospital):
            doctorhospital_values = '#<>#'.join([
                item['sk'], item.get('doctor_id',''),item.get('hospital_location',''), item.get('hospital_link',''), item.get('hospital_name',''), item.get('hospital_rating',''), item.get('hospital_address',''), item.get('hospital_monday_timing',''), item.get('hospital_tuesday_timing',''), item.get('hospital_wednesday_timing',''), item.get('hospital_thursday_timing',''), item.get('hospital_friday_timing',''), item.get('hospital_saturday_timing',''), item.get('hospital_sunday_timing',''), item.get('hospital_consultation_fee',''), item.get('hospital_practo_gurantee',''), item.get('hospital_photos','') , item.get('hospital_booking_type',''), item.get('hospital_latitude',''), item.get('hospital_longitude',''), item.get('reference_url',''), item.get('aux_info','')
                ])
            spider.get_doctorhospital_file().write('%s\n' %doctorhospital_values)
            spider.get_doctorhospital_file().flush()
            self.write_item_into_avail_file(item, spider,'doctorhospital')


        return item
